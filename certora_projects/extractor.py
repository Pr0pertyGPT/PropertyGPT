import csv
import hashlib
import os
import re
import openai
import pandas as pd
from tqdm import tqdm

from contract_extractor import extract_state_variables_from_code
def find_functions(file_path):
    # 匹配函数声明，包括可能跨行的参数列表
    function_pattern = re.compile(r"function\s+(\w+)[\s\S]*?\{", re.DOTALL)

    functions = []
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return functions

    with open(file_path, "r", encoding="utf-8") as file:
        contract_lines = file.readlines()

    contract_data = "".join(contract_lines)

    for match in function_pattern.finditer(contract_data):
        function_name = match.group(1)
        start_line = contract_data[:match.start()].count("\n") + 1

        # 查找函数体的结束，正确处理嵌套的大括号
        open_brackets = 1
        end_line_index = match.end()
        while end_line_index < len(contract_data) and open_brackets > 0:
            if contract_data[end_line_index] == '{':
                open_brackets += 1
            elif contract_data[end_line_index] == '}':
                open_brackets -= 1
            end_line_index += 1

        end_line = contract_data[:end_line_index].count("\n") + 1
        function_body = contract_lines[start_line - 1:end_line]

        functions.append((function_name, start_line, end_line, function_body))

        # print(f"Function: {function_name}, Start line: {start_line}, End line: {end_line}")

    if not functions:
        print(f"No functions found in {file_path}.")

    return functions
def find_methods_in_block(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []

    with open(file_path, "r", encoding="utf-8") as file:
        contract_data = file.read()

    methods_block_pattern = re.compile(r"methods\s*\{[\s\S]*?\}", re.DOTALL)
    method_name_pattern = re.compile(r"^\s*([a-zA-Z0-9_\.]+)\(", re.MULTILINE)

    methods_match = methods_block_pattern.search(contract_data)
    methods = []
    new_methods=[]
    if methods_match:
        methods_block = methods_match.group()
        methods = method_name_pattern.findall(methods_block)
        new_methods = [method for method in methods if method not in ['require', 'assert']]
    return new_methods


def find_code_blocks(file_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    patterns = {
        'invariant': re.compile(r"invariant\s+(\w+)[\s\S]*?\{", re.DOTALL),
        'rule': re.compile(r"rule\s+(\w+)[\s\S]*?\{", re.DOTALL)
    }

    code_blocks = []
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return code_blocks

    methods = find_methods_in_block(file_path)
    
    with open(file_path, "r", encoding="utf-8") as file:
        contract_lines = file.readlines()

    contract_data = "".join(contract_lines)

    for block_type, pattern in patterns.items():
        for match in pattern.finditer(contract_data):
            block_name = match.group(1)
            start_line = contract_data[:match.start()].count("\n") + 1
            open_brackets = 1
            end_line_index = match.end()
            while end_line_index < len(contract_data) and open_brackets > 0:
                if contract_data[end_line_index] == '{':
                    open_brackets += 1
                elif contract_data[end_line_index] == '}':
                    open_brackets -= 1
                end_line_index += 1

            end_line = contract_data[:end_line_index].count("\n") + 1
            block_content = contract_lines[start_line - 1:end_line]

            # 检查方法名是否在此代码块中
            methods_in_block = [method for method in methods if method in "".join(block_content)]

            code_blocks.append({
                'file_path': file_path,
                'block_type': block_type,
                'block_name': block_name,
                'start_line': start_line,
                'end_line': end_line,
                'block_content': block_content,
                'methods_in_block': methods_in_block
            })

    if not code_blocks:
        print(f"No code blocks found in {file_path}.")

    return code_blocks
def has_function_calls(function_body):
    if "view" in str(function_body).lower():
        return False  # Skip view functions
    # Extract the content between the first opening and last closing curly braces
    match = re.search(r'\{(.*)\}', function_body, re.DOTALL)
    if not match:
        return False  # No function body found

    inner_body = match.group(1)

    # Regular expression to find method calls (e.g., .method())
    method_call_pattern = re.compile(r'\.\s*(\w+)\s*\(')
    method_calls = method_call_pattern.findall(inner_body)

    if not method_calls:
        return False  # No method calls found

    # Check if all method calls are either 'balanceOf' or 'totalsupply'
    allowed_methods = {'balanceOf', 'totalSupply'}
    for method_name in method_calls:
        if method_name not in allowed_methods:
            return True  # Found a method call that is not 'balanceOf' or 'totalsupply'

    return False  # Only 'balanceOf' or 'totalsupply' method calls found

def get_responses(prompt):
    return get_responses_gpt4([prompt])[0]
        
def get_responses_gpt4(prompts):
    responses = []
    openai.api_key = os.getenv("OPENAI_API_KEY")
    openai.api_base="https://api.openai.com/v1"
    
    for prompt in prompts:
        message = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-1106",
            messages=message
        )
        responses.append(completion.choices[0].message.content)
        
    return responses

def format_and_write_to_csv(code_blocks):
    existing_hashes = set()
    
    with open('output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL, escapechar='\\')
        # 定义 CSV 列标题
        headers = ['SpecHash','SpecIndex', 'Type', 'Name', 'StartLine', 'EndLine', 'MethodsInRule', 'RuleContent', 'RelatedFunctions', 'FunctionBodies', 'FilePath','ContractCode', 'StateVarAssignment','RuleContentNL']
        writer.writerow(headers)

        if not code_blocks:
            writer.writerow(["No code blocks found."])
            return

        for index, block in tqdm(enumerate(code_blocks, start=1)):
            blockhash=block['block_hash']
            if blockhash in existing_hashes:
                continue  # 跳过已存在的 block_hash
            # 将规则内容和相关函数整合为单个字符串
            rule_content = ''.join(block['block_content'])
            related_functions = ''
            function_bodies = ''
            state_var_assignment = 'No'  # Default value
            for func in block.get('related_functions', []):
                related_functions += f"{func[0]} (Lines {func[1]}-{func[2]}), "
                function_body = ''.join(func[3])
                function_bodies += function_body
                # Check if the function is a state variable assignment function
                if check_function_code_if_statevar_assign(function_body, block['contract_code']) or has_function_calls(function_body):
                    state_var_assignment = 'Yes'
            block['contract_code']=block['contract_code'].replace('\n','')
            prompt_ask_rulecontent_NL=rule_content + " tell me in what this rule/invariant needs to be verified."
            print("asking GPT-3 for rule content NL...")
            res=""
            # res=get_responses(prompt_ask_rulecontent_NL)
            
            # 写入每个代码块的数据
            writer.writerow([
                block['block_hash'],
                index,
                block['block_type'],
                block['block_name'],
                block['start_line'],
                block['end_line'],
                ', '.join(set(method for method in block['methods_in_block'] if method != 'ssert')),
                rule_content,
                related_functions,
                function_bodies,
                block['file_path'],
                "",
                state_var_assignment,
                str(res)  # Add this value to the row
            ])
def update_blocks_with_cross_references(code_blocks):
    def find_block_by_name(name):
        for block in code_blocks:
            if block['block_name'] == name:
                return block
        return None

    def update_block_content(block, visited=None):
        if visited is None:
            visited = set()

        if block['block_name'] in visited:
            return []

        visited.add(block['block_name'])
        updated_content = []

        for line in block['block_content']:
            if line not in updated_content:
                updated_content.append(line)  # Avoids duplicate lines

            for other_block in code_blocks:
                if other_block['block_name'] in line and other_block['block_name'] != block['block_name']:
                    referenced_block = find_block_by_name(other_block['block_name'])
                    if referenced_block:
                        ref_block_content = update_block_content(referenced_block, visited)
                        for ref_line in ref_block_content:
                            if ref_line not in updated_content:
                                updated_content.append(ref_line)  # Adds new content from referenced blocks, avoiding duplicates

        return updated_content

    for block in code_blocks:
        block['block_content'] = update_block_content(block)
        # Assuming find_methods_in_block_from_content is a predefined function
        block['methods_in_block'] = find_methods_in_block_from_content(block['block_content'])



def find_methods_in_block_from_content(content):
    method_name_pattern = re.compile(r"(?!require|assert)([a-zA-Z0-9_\.]+)\(", re.MULTILINE)
    methods = method_name_pattern.findall("".join(content))
    return methods
def check_function_code_if_statevar_assign(function_code,contract_code):
    state_vars=extract_state_variables_from_code(contract_code)
    nodes = function_code.split(';')
    # 判断每个操作是否是对状态变量的赋值
    for node in nodes:
        if '=' in node:
            # 获取等号左边的内容
            left_side = node.split('=')[0].strip()
            # 检查是否有状态变量
            for var in state_vars:
                if re.search(r'\b' + re.escape(var) + r'\b', left_side):
                    return True
    return False

def process_spec_files(folder_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    code_blocks_dataset = []

    for root, dirs, files in tqdm(os.walk(folder_path), desc="Processing spec files"):
        for file_name in files:
            if file_name.endswith('.spec'):
                
                file_path = os.path.join(root, file_name)
                code_blocks = find_code_blocks(file_path)
                update_blocks_with_cross_references(code_blocks)
                code_blocks_dataset.extend(code_blocks)
    return code_blocks_dataset
def generate_hash_for_block(block):
    # Generate a hash for the block based on its content
    block_content_string = str(block)
    return hashlib.md5(block_content_string.encode()).hexdigest()
def find_and_add_functions_to_code_blocks(folder_path, code_blocks_dataset):
    sol_functions, contract_codes = collect_all_functions(folder_path)
    
    # Prepare a temporary dataset for cloned blocks
    cloned_blocks_dataset = []

    for block in code_blocks_dataset:
        # Generate and assign a unique identifier (hash) to each block
        block_hash = generate_hash_for_block(block)
        block['block_hash'] = block_hash

        for function_name, function_details in sol_functions.items():
            # Check if the function is in the current block's methods
            methods_in_block = [method for method in block['methods_in_block'] if method.endswith('.' + function_name) or method == function_name]

            if methods_in_block:
                cloned_block = block.copy()
                cloned_block['related_functions'] = [function_details]  # Include only this function
                cloned_block['contract_code'] = contract_codes[function_name]
                cloned_block['methods_in_block'] = methods_in_block  # Include only relevant methods

                # The cloned block shares the same hash as the original block
                cloned_block['block_hash'] = block_hash

                # Add the cloned block to the dataset
                cloned_blocks_dataset.append(cloned_block)

    # Replace original dataset with cloned blocks dataset
    code_blocks_dataset[:] = cloned_blocks_dataset                                    
def collect_all_functions(folder_path):
    sol_functions = {}
    contract_codes = {}  # To store contract code for each function

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.sol') and not file_name.endswith('.t.sol') and not file_name.startswith('I'):
                sol_file_path = os.path.join(root, file_name)
                with open(sol_file_path, "r", encoding="utf-8") as file:
                    contract_code = file.read()
                functions = find_functions(sol_file_path)
                for function in functions:
                    sol_functions[function[0]] = function
                    contract_codes[function[0]] = contract_code
    return sol_functions, contract_codes

def add_recursive_functions(sol_functions, block, method_name, depth, added_functions, contract_codes):
    if method_name not in sol_functions or depth > 2:
        return

    function_body = sol_functions[method_name][3]
    for line in function_body:
        for func_name in sol_functions:
            if func_name in line and func_name != method_name and func_name not in added_functions:
                block['related_functions'].append(sol_functions[func_name])
                added_functions.add(func_name)
                # Add the contract code of the recursively found function
                block['contract_code'].add(contract_codes[func_name])
                add_recursive_functions(sol_functions, block, func_name, depth + 1, added_functions, contract_codes)
def find_sol_files_in_directory(directory_path):
    sol_files = []
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.sol'):
                sol_files.append(os.path.join(root, file))
    return sol_files

def process_and_merge_spec_files(folder_paths):
    combined_code_blocks_dataset = []
    
    for folder_path in tqdm(folder_paths,"Processing spec folders"):
        print("Processing spec folder...",folder_path)
        code_blocks_dataset = process_spec_files(folder_path)

        # Recursively find .sol files in the folder and its subfolders
        sol_files = find_sol_files_in_directory(folder_path)
        if sol_files:
            find_and_add_functions_to_code_blocks(folder_path, code_blocks_dataset)
        else:
            print(f"No .sol files found in the folder: {folder_path}")

        combined_code_blocks_dataset.extend(code_blocks_dataset)

    return combined_code_blocks_dataset
def combine_rows_by_spechash_exclude_no(input_file, output_file):
    # 读取CSV文件
    df = pd.read_csv(input_file)

    # 过滤掉StateVarAssignment列为'No'的行
    df_filtered = df[df['StateVarAssignment'] != 'No']

    # 对数据按照SpecHash分组
    grouped = df_filtered.groupby('SpecHash')

    # 为每个组合并行
    combined_rows = []
    for name, group in grouped:
        combined_row = group.iloc[0].copy()  # 从第一行开始，用于累积合并
        for column in group.columns:
            if group[column].nunique() > 1:  # 如果该列在组内有不同的值
                combined_row[column] = ' | '.join(group[column].astype(str).unique())  # 合并不同的值
        combined_rows.append(combined_row)

    # 创建一个新的DataFrame并保存到CSV
    combined_df = pd.DataFrame(combined_rows)
    combined_df.to_csv(output_file, index=False)

def main(folder_paths):
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    combined_code_blocks_dataset = process_and_merge_spec_files(folder_paths)
    
    format_and_write_to_csv(combined_code_blocks_dataset)

# Your folder paths
# 训练集
folder_paths = [
    './aave_l2_bridge',
    './aave_proof_of_reserve',
    './aave_rescue_mission',
    './aave_staked_token',
    './aave_starknet_bridge',
    './aave_static_token',
    './aave_v2',
    './aave_v3',
    './aave_vault',
    './celo_governance',
    './compound_moneymarket',
    './furucombo',
    './gho-core',
    './keep_fully',
    './lido_v2',
    './notional_finance_v2',
    './openzepplin',
    './opyn_gamma_protocol',
    './ousd',
    './popsicle_v3_optimizer',
    './radicle_drips',
    './rocket_joe',
    './sushi_benttobox',
]
# 测试集
# folder_paths=[
#     './rocket_joe',
#     './radicle_drips',
#     './lido_v2'
# ]

main(folder_paths)
combine_rows_by_spechash_exclude_no('output.csv', 'combined_output_train_all.csv')