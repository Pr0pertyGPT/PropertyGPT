
1. There are 623 in total, and 9 projects are randomly selected. If there are not enough specs for a certain project to be included in the test set, select other projects.

Project selection result details:
[combied_output_train_all_with_functionality_sampled -1-.csv](assets/combied_output_train_all_with_functionality_sampled%20-1-.csv)


data：

|Project|count|
| ----- | ----- |
|aave\_proof\_of\_reserve|3|
|aave\_v3|17|
|celo\_governance|10|
|furucombo|10|
|openzepplin|10|
|opyn\_gamma\_protocol|10|
|ousd|10|
|radicle\_drips|10|
|sushi\_benttobox|10|

1. According to the selected spec, enter the original function and generate a new spec. This excludes the possibility of using the spec knowledge of the same project to generate, ensuring that the functions and knowledge used come from two different sources. s project
2. The results of manual + gpt marking are as follows:
[project_dimension -1- -3-.xlsx](assets/project_dimension%20-1-%20-3-.xlsx)


3. After marking, mark whether the originally selected spec has a corresponding TP according to the marking results.
[combied_output_train_all_with_functionality_sampled -2-.xlsx](assets/combied_output_train_all_with_functionality_sampled%20-2-.xlsx)



4. According to the results according to the project, if the spec does not hit, it is equivalent to FN.

|Project|spec num|hit|Recall|note|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|3|1| |
|aave\_v3|17|15|0.882352941| |
|celo\_governance|10|10|1| |
|furucombo|10|7|0.7| |
|openzepplin|10|1|0.1|After taking a look, It actually retrieved 8 rules, but 6 of them were openzeppelin’s own knowledge, so I skipped them.|
|opyn\_gamma\_protocol|10|8|0.8| |
|ousd|10|10|1| |
|radicle\_drips|10|7|0.7| |
|sushi\_benttobox|10|10|1| |
|total|90|71|0.788888889| |

5. TP/FP

[project_dimension -1- -3- -1-.xlsx](assets/project_dimension%20-1-%20-3-%20-1-.xlsx)




FP:36,TP:344

Number of hits



TP/FP at project level

|Project|TP|FP|Precision|
| ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|34|4|0.894736842|
|aave\_v3|53|8|0.868852459|
|celo\_governance|37|2|0.948717949|
|furucombo|21|2|0.913043478|
|openzepplin|2|0|1|
|opyn\_gamma\_protocol|25|5|0.833333333|
|ousd|94|6|0.94|
|radicle\_drips|16|1|0.941176471|
|sushi\_benttobox|62|8|0.885714286|
|总计|344|36|0.905263158|

# 0420：
By project, the newly added TP of non-factual errors, TP and FP of TOP-k are not considered:

Project level:

Number of hits:

|Count| | | | | | | | | | | |
| ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- | ----- |
|Project|top-1|top-2|top-3|top-4|top-5|top-6|top-7|top-8|top-9|top-max|总计groundtruth|
|aave\_proof\_of\_reserve|2|3|3|3|3|3|3|3|3|3|3|
|aave\_v3|11|12|13|13|14|14|14|14|14|15|17|
|celo\_governance|8|9|9|9|9|9|9|9|9|10|10|
|furucombo|6|7|7|7|7|7|7|7|7|7|10|
|openzepplin|1|1|1|1|1|1|1|1|1|1|10|
|opyn\_gamma\_protocol|4|4|5|6|6|6|6|6|6|8|10|
|ousd|5|6|8|8|8|8|8|8|8|10|10|
|radicle\_drips|4|6|6|6|6|6|6|6|6|7|10|
|sushi\_benttobox|6|10|10|10|10|10|10|10|10|10|10|
|总计|47|58|62|63|64|64|64|64|64|71|90|
|Recall| | | | | | | | | | | |
|Project|top-1|top-2|top-3|top-4|top-5|top-6|top-7|top-8|top-9|top-max|总计groundtruth|
|aave\_proof\_of\_reserve|0.67|1.00|1.00|1.00|1.00|1.00|1.00|1.00|1.00|1.00|3|
|aave\_v3|0.65|0.71|0.76|0.76|0.82|0.82|0.82|0.82|0.82|0.88|17|
|celo\_governance|0.80|0.90|0.90|0.90|0.90|0.90|0.90|0.90|0.90|1.00|10|
|furucombo|0.60|0.70|0.70|0.70|0.70|0.70|0.70|0.70|0.70|0.70|10|
|openzepplin|0.10|0.10|0.10|0.10|0.10|0.10|0.10|0.10|0.10|0.10|10|
|opyn\_gamma\_protocol|0.40|0.40|0.50|0.60|0.60|0.60|0.60|0.60|0.60|0.80|10|
|ousd|0.50|0.60|0.80|0.80|0.80|0.80|0.80|0.80|0.80|1.00|10|
|radicle\_drips|0.40|0.60|0.60|0.60|0.60|0.60|0.60|0.60|0.60|0.70|10|
|sushi\_benttobox|0.60|1.00|1.00|1.00|1.00|1.00|1.00|1.00|1.00|1.00|10|
|平均|0.52|0.64|0.69|0.70|0.71|0.71|0.71|0.71|0.71|0.79|1|

top-5：

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|11|4|0.733333333|
|aave\_v3|14|29|26|0.527272727|
|celo\_governance|9|27|9|0.75|
|furucombo|7|10|9|0.526315789|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|13|15|0.464285714|
|ousd|8|22|14|0.611111111|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|25|14|0.641025641|
|总计| |148|99|0.599190283|

top-4：

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|9|3|0.75|
|aave\_v3|13|25|23|0.520833333|
|celo\_governance|9|26|8|0.764705882|
|furucombo|7|10|8|0.555555556|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|10|14|0.416666667|
|ousd|8|17|12|0.586206897|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|20|13|0.606060606|
|总计| |128|89|0.589861751|

TOP-3:



|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|7|2|0.777777778|
|aave\_v3|13|23|17|0.575|
|celo\_governance|9|20|6|0.769230769|
|furucombo|7|9|8|0.529411765|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|5|7|12|0.368421053|
|ousd|8|14|8|0.636363636|
|radicle\_drips|6|9|7|0.5625|
|sushi\_benttobox|10|16|11|0.592592593|
|总计| |107|71|0.601123596|

TOP-6:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|14|4|0.777777778|
|aave\_v3|14|31|26|0.543859649|
|celo\_governance|9|28|9|0.756756757|
|furucombo|7|11|9|0.55|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|14|15|0.482758621|
|ousd|8|26|17|0.604651163|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|27|15|0.642857143|
|总计| |162|103|0.611320755|

TOP-7:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|16|5|0.761904762|
|aave\_v3|14|31|28|0.525423729|
|celo\_governance|9|28|10|0.736842105|
|furucombo|7|11|10|0.523809524|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|14|16|0.466666667|
|ousd|8|29|21|0.58|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|29|16|0.644444444|
|总计| |169|114|0.597173145|

TOP-8:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|18|6|0.75|
|aave\_v3|14|31|29|0.516666667|
|celo\_governance|9|29|10|0.743589744|
|furucombo|7|11|11|0.5|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|14|16|0.466666667|
|ousd|8|33|23|0.589285714|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|32|16|0.666666667|
|总计| |179|119|0.600671141|

TOP-9:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|18|8|0.692307692|
|aave\_v3|14|32|29|0.524590164|
|celo\_governance|9|29|10|0.743589744|
|furucombo|7|11|12|0.47826087|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|6|14|16|0.466666667|
|ousd|8|37|25|0.596774194|
|radicle\_drips|6|9|8|0.529411765|
|sushi\_benttobox|10|35|16|0.68627451|
|总计| |187|124|0.601286174|

TOP-MAX:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|25|13|0.657894737|
|aave\_v3|15|32|29|0.524590164|
|celo\_governance|10|29|10|0.743589744|
|furucombo|7|11|12|0.47826087|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|8|14|16|0.466666667|
|ousd|10|67|33|0.67|
|radicle\_drips|7|9|8|0.529411765|
|sushi\_benttobox|10|49|21|0.7|
|总计| |238|142|0.626315789|

TOP-1:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|2|2|1|0.666666667|
|aave\_v3|11|11|5|0.6875|
|celo\_governance|8|8|1|0.888888889|
|furucombo|6|6|4|0.6|
|openzepplin|1|1|0|1|
|opyn\_gamma\_protocol|4|4|3|0.571428571|
|ousd|5|5|3|0.625|
|radicle\_drips|4|4|5|0.444444444|
|sushi\_benttobox|6|6|4|0.6|
|总计| |47|26|0.643835616|

TOP-2:

|Project|Hit groundtruth number|TP|FP|Precision|
| ----- | ----- | ----- | ----- | ----- |
|aave\_proof\_of\_reserve|3|5|1|0.833333333|
|aave\_v3|12|19|10|0.655172414|
|celo\_governance|9|16|2|0.888888889|
|furucombo|7|9|6|0.6|
|openzepplin|1|2|0|1|
|opyn\_gamma\_protocol|4|5|9|0.357142857|
|ousd|6|8|7|0.533333333|
|radicle\_drips|6|9|5|0.642857143|
|sushi\_benttobox|10|14|6|0.7|
|总计| |87|46|0.654135338|

# Time data
Does not include failure reasons
[fix info -2-.xlsx](assets/fix%20info%20-2-.xlsx)


include failure reasons

[fix info -1- -1-.xlsx](assets/fix%20info%20-1-%20-1-.xlsx)



Frequency of generation

|Generation times|count|
| ----- | ----- |
|1|234|
|2|40|
|3|18|
|4|10|
|5|7|
|6|5|
|7|2|
|8|2|
|9|2|
|10|1|
|11|49|

Generation time (segmented)

|period|count|
| ----- | ----- |
|0-9|12|
|10-19|83|
|20-29|89|
|30-39|44|
|40-49|44|
|50-59|29|
|60-69|15|
|70-79|11|
|80-89|6|
|90-99|3|
|100-119|10|
|120-139|4|
|140-159|6|
|160-179|2|
|180-199|2|
|200-249|2|
|300-349|4|
|350-399|2|
|400-450|2|

Failure reason list

Cause distribution

|Undeclared identifier.|38|
| ----- | ----- |
|Expected ';' but got '}'|8|
|msg.value and "callvalue()" can only be used in sth|3|

|Generate data\_If there are too many repairs, the last error message will be reported.|
| ----- |
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Expected ';' but got '}'|
|msg.value and "callvalue()" can only be used in sth|
|Expected ';' but got '}'|
|Expected ';' but got '}'|
|Undeclared identifier.|
|Undeclared identifier.|
|Expected ';' but got '}'|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Expected ';' but got '}'|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|msg.value and "callvalue()" can only be used in sth|
|msg.value and "callvalue()" can only be used in sth|
|Expected ';' but got '}'|
|Undeclared identifier.|
|Undeclared identifier.|
|Undeclared identifier.|
|Expected ';' but got '}'|
|Undeclared identifier.|
|Expected ';' but got '}'|
|Undeclared identifier.|

