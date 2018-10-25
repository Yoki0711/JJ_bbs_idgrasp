
import csv
from collections import Counter

print("————以下文件名均不加任何表达格式的后缀————")
file_name = input("请输入希望统计的文件名：") + ".csv"
file_count = input("请输入【统计id出现次数的文件】的文件名：") + ".csv"
file_stat = input("请输入【整理所有id发言的文件】的文件名：") + ".csv"

# 新建文件，存放整理后的数据
with open(file_stat, 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', '发言时间', '发言内容', '楼层号'])

# 读取csv文件，统计id数量
# fieldname统一为id、发言时间、发言内容、楼层号
def dict_rearrange():
    """
    输入：
    输出：字典：{id：出现次数} 按出现次数从大到小排序
    """
    sel_lst = []
    with open(file_name, "r", encoding='utf-8', newline='') as csvfile:
        dict_reader = csv.DictReader(csvfile)
        for row in dict_reader:
            sel_lst.append(row["id"])
        count_dict = Counter(sel_lst)
        sort_dict = sorted(count_dict.items(), key=lambda d: d[1], reverse= True)
        sort_count_dict = dict(sort_dict)
        return sort_count_dict

# print(dict_rearrange("1501433.csv"))

# 将出现次数>1的id和其次数整理成csv文件
def stat_id(count_dict, file_count):
    """
    输入：字典：{id：aaa, 重复次数:bbb}
    输出：csv文件。fieldname：id，统计次数
    """
    new_dict = {}
    for spe_id, spe_times in count_dict.items():
        if spe_times > 1:
            new_dict[spe_id] = spe_times  # 创建新的字典，仅包含发言次数>1的id
    with open(file_count, 'a', newline='') as cnt:
        writer = csv.writer(cnt)
        writer.writerow(["id", "发言次数"])
        for key, value in new_dict.items():
            writer.writerow([key, value])

# print(stat_id(dict_rearrange("1501433.csv"), "aaaa.csv"))

# 将出现次数>1的id按出现次数降序排列，输出为csv文件
def order_id(count_dict, file_stat):
    """
    输入：按counter方法整理好的字典
    输出：csv文件。fieldname：id、发言时间、发言内容、楼层号
        包含所有id，按发言次数排序
    """
    with open(file_stat, 'a', newline='') as f:
        writer = csv.writer(f)
        for spe_id in count_dict:
            with open(file_name, "r", encoding='utf-8', newline='') as csvfile:
                dict_reader = csv.DictReader(csvfile)
                for row in dict_reader:
                    if spe_id == row["id"]:
                        writer.writerow([row['id'], row['发言时间'], row['发言内容'], row['楼层号']])

# print(order_id("1501433.csv",dict_rearrange("1501433.csv"), "bbb.csv"))

# 整理所有函数
def main():
    count_dict = dict_rearrange()
    stat_id(count_dict, file_count)
    order_id(count_dict, file_stat)

# 执行函数
if __name__ == '__main__':
    main()