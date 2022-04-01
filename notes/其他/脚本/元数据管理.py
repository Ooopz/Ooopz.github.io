import os
import re
import time
import frontmatter

def update_front_matter(
    file, 
    update_modify_time=False, 
    add_tag:list=None, clear_all_tag=False, del_tag:list=None, 
    add_meta:dict=None, del_meta:list=None
):
    """修改yamal格式的frontmatter
    file: 要处理的文件路径
    update_modify_time: 是否更新最后编辑时间
    add_tag: 要添加的标签列表
    clear_all_tag: 是否清除所有tag
    del_tag: 删除指定列表的标签
    add_meta: 添加元数据项目
    del_meta: 删除指定列表的元数据项目
    """
    
    is_write = False
    
    with open(file, 'r', encoding='utf-8') as f:
        post = frontmatter.loads(f.read())
    
    # 更新文件修改时间
    if update_modify_time:
        if not post.metadata.get('modify_date', None):
            timeArray = time.localtime((os.path.getmtime(file)))
            post['modify_date'] = time.strftime("%Y-%m-%d %H:%M", timeArray)
            print(f'更新后修改时间为: {time.strftime("%Y-%m-%d %H:%M", timeArray)}')
            is_write = True
    
    # 标签操作
    exist_tags = post.get("tags", [])
    if isinstance(exist_tags, str):
        exist_tags = [tag for tag in exist_tags.replace(',',' ').split(" ") if tag != ""]
    new_tags = exist_tags.copy()
    
    if add_tag is not None:
        new_tags = new_tags + add_tag
    if del_tag is not None:
        new_tags = [tag for tag in new_tags if tag not in del_tag]
    if clear_all_tag:
        new_tags = []
    
    if set(new_tags) != set(exist_tags):
        new_tags = list(set(new_tags))
        new_tags.sort()
        post['tags'] = new_tags
        print(f'当前文件tag有: {exist_tags}, 修改后文件标签有: {new_tags}')
        is_write = True
    
    # 元数据项目操作
    exist_keys = list(post.metadata.keys())

    if add_meta is not None:
        post.metadata.append(add_meta)
    if del_meta is not None:
        for meta in del_meta:
            post.metadata.pop(meta, None)
    
    new_keys = list(post.metadata.keys())
    print(exist_keys)
    print(new_keys)
    if set(new_keys)!=set(exist_keys):
        print(f'当前文件元数据项目有: {exist_keys}, 修改后文件元数据项目有: {new_keys}')
        is_write = True
    
    # 标签写入
    if is_write:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(frontmatter.dumps(post))


def list_all_md(root_path, ignore_dirs=[]):
    """
    生成md文件列表
    """
    files = []
    default_dirs = [".git", ".obsidian", ".config", ".stfolder", ".trash"]
    ignore_dirs.extend(default_dirs)

    for parent, dirs, filenames in os.walk(root_path):
        dirs[:] = [d for d in dirs if not d in ignore_dirs]
        filenames = [f for f in filenames if not f[0] == '.']
        for file in filenames:
            if file.endswith(".md"):
                files.append(os.path.join(parent, file))
    return files


if __name__ == "__main__":

    files = list_all_md(r'C:\Users\Tking\Documents\MyCode\MyNote\编程\Python\源码详解')
    for file in files:
        
        print("---------------------------------------------------------------")
        print('当前文件: ', file)
        
        # update_front_matter(file, del_meta=['tags','author','Update Time','Last Edit Time'])
        update_front_matter(file, add_tag=['Python/源码详解'])