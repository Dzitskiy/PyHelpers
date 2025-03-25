import os
import argparse
import xml.etree.ElementTree as ET
from collections import defaultdict

def get_net_versions(file_path):
    """Извлекает версии .NET из файла проекта"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            tree = ET.parse(f)
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='utf-16') as f:
                tree = ET.parse(f)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return []
    except ET.ParseError as e:
        print(f"XML parse error in {file_path}: {e}")
        return []
    except Exception as e:
        print(f"Error opening {file_path}: {e}")
        return []
    
    root = tree.getroot()
    frameworks = []

    for elem in root.iter():
        tag = elem.tag.split('}', 1)[-1]
        if tag in ('TargetFramework', 'TargetFrameworks'):
            if elem.text:
                values = [v.strip() for v in elem.text.split(';')]
                frameworks.extend(values)
    
    return list(set(frameworks))

def scan_projects(root_dir):
    """Сканирует каталог и группирует проекты по первому уровню вложенности"""
    root_dir = os.path.abspath(root_dir)
    groups = defaultdict(list)
    
    for dirpath, _, files in os.walk(root_dir):
        for file in files:
            if not file.lower().endswith(('.csproj', '.vbproj', '.fsproj')):
                continue
                
            file_path = os.path.join(dirpath, file)
            rel_dir = os.path.relpath(os.path.dirname(file_path), root_dir)
            
            # Определяем группу первого уровня
            if rel_dir == '.':
                group_name = 'ROOT'
            else:
                group_name = rel_dir.split(os.sep, 1)[0].upper()
            
            project_name = os.path.splitext(file)[0]
            versions = get_net_versions(file_path)
            version_str = ', '.join(versions) if versions else 'Not found'
            
            groups[group_name].append((version_str, project_name))
    
    # Сортируем группы и проекты
    for group in sorted(groups.keys()):
        projects = groups[group]
        max_version_len = max(len(ver) for ver, _ in projects)
        
        print(f"\n[{group}]")
        for ver, name in sorted(projects, key=lambda x: x[1].lower()):
            print(f"  {ver:<{max_version_len}} | {name}")

def main():
    parser = argparse.ArgumentParser(description='Find .NET projects grouped by first-level directories')
    parser.add_argument('path', nargs='?', default='.', 
                      help='Path to scan (default: current directory)')
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path '{args.path}' does not exist")
        return
        
    if not os.path.isdir(args.path):
        print(f"Error: '{args.path}' is not a directory")
        return

    scan_projects(os.path.abspath(args.path))

if __name__ == "__main__":
    main()