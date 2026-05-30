#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
展示资源管理模块的模板文件
"""
import os


def print_file(file_path, title):
    """打印文件内容"""
    print(f"\n{'=' * 70}")
    print(f"  {title}")
    print(f"{'=' * 70}\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # 截取前150行
        lines = content.split('\n')[:150]
        print('\n'.join(lines))
        if len(lines) < len(content.split('\n')):
            print(f"\n... (文件更长，已截取前 {len(lines)} 行)")


def main():
    """主函数"""
    print("\n")
    print("╔" + "═" * 68 + "╗")
    print("║" + " " * 25 + "资源管理模块模板展示" + " " * 25 + "║")
    print("╚" + "═" * 68 + "╝")
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, "sql", "templates", "resource")
    
    templates = [
        ("idc_list.html", "1. 机房列表页面"),
        ("server_list.html", "2. 服务器列表页面"),
        ("project_list.html", "3. 项目列表页面"),
        ("cluster_list.html", "4. 集群列表页面"),
        ("resource_instance_list.html", "5. 实例资源关联列表"),
        ("resource_instance_edit.html", "6. 实例资源关联编辑页面"),
    ]
    
    for filename, title in templates:
        file_path = os.path.join(templates_dir, filename)
        print_file(file_path, title)


if __name__ == "__main__":
    main()
