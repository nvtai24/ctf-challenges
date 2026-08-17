import os
import re

def refactor_file(filepath):
    print(f"Refactoring {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        replacements = {
            r"## Sự miêu tả": "## Mô tả",
            r"## Lỗ hổng": "## Lỗ hổng bảo mật",
            r"## Khai thác(\s|\().*": "## Khai thác (Exploit)",
            r"Cờ:": "Flag:",
            r"tải trọng": "payload",
            r"Tải trọng": "Payload",
            r"tập lệnh": "script",
            r"Tập lệnh": "Script",
            r"bản in rò rỉ": "địa chỉ bị lộ (leak)",
            r"rò rỉ": "leak",
            r"phần bù": "offset",
            r"địa chỉ cơ sở": "base address",
            r"Cơ sở": "Base",
            r"tràn bộ đệm tiêu chuẩn": "lỗi buffer overflow cơ bản",
            r"trình bao tương tác": "interactive shell",
            r"truyền tải đường dẫn": "path traversal",
            r"vượt qua": "bypass",
            r"Nó hoạt động như thế nào": "Cách hoạt động",
            r"bị xử tử": "bị thực thi",
            r"xử tử": "thực thi",
            r"xác nhận": "kiểm tra",
            r"byte ma thuật": "magic bytes",
            r"giảm thiểu": "Biện pháp phòng ngừa (Mitigation)",
            r"Giảm thiểu": "Biện pháp phòng ngừa (Mitigation)",
            r"quản trị viên ẩn": "hidden admin",
            r"tình trạng cuộc đua": "race condition",
            r"lỗ hổng giả mạo": "lỗ hổng forgery",
            r"địa chỉ băm": "địa chỉ hash",
            r"băm": "hash",
            r"chuỗi định dạng": "format string",
            r"ngăn xếp": "stack",
            r"đống": "heap",
            r"con trỏ lệnh": "instruction pointer (RIP)",
            r"cơ sở dữ liệu": "database",
            r"máy chủ": "server",
            r"phần mở rộng": "file extension",
            r"tiện ích mở rộng": "file extension",
            r"khách hàng": "client",
            r"yêu cầu HTTP": "HTTP request",
        }
        
        blocks = re.split(r'(```.*?```|`.*?`)', content, flags=re.DOTALL)
        
        new_blocks = []
        for i, block in enumerate(blocks):
            if i % 2 == 0:
                for pattern, repl in replacements.items():
                    block = re.sub(pattern, repl, block)
            new_blocks.append(block)
            
        new_content = "".join(new_blocks)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
    except Exception as e:
        print(f"Failed to process {filepath}: {e}")

if __name__ == '__main__':
    base_dir = r"c:\Users\Nvtai\Desktop\ctf-challenges"
    
    files_to_refactor = []
    
    files_to_refactor.append(os.path.join(base_dir, "CTF_COMPLETE_GUIDE.md"))
    files_to_refactor.append(os.path.join(base_dir, "CTF_SOLUTIONS_SUMMARY.md"))
    
    for folder in sorted(os.listdir(base_dir)):
        if re.match(r'^\d{2}-', folder):
            solution_path = os.path.join(base_dir, folder, "SOLUTION.md")
            if os.path.exists(solution_path):
                files_to_refactor.append(solution_path)
                
    for filepath in files_to_refactor:
        refactor_file(filepath)
    print("Done refactoring terms.")
