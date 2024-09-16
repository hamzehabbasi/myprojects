import os

current_directory = os.getcwd()

for filename in os.listdir(current_directory):
    if filename.endswith('.txt'):
        file_path = os.path.join(current_directory, filename)

        with open(file_path, 'r') as file:
            lines = file.readlines()


        seen_strings = {}
        unique_lines = []

        for line in lines:
            line = line.strip()
            if ':' in line:
                key = line.split(':', 1)[0]
                if key not in seen_strings:
                    seen_strings[key] = line
                    unique_lines.append(line)


        with open(file_path, 'w') as file:
            for line in unique_lines:
                file.write(line + '\n')

print("خطوط تکراری  حذف شدند و فایل‌ها به‌روزرسانی شدند.")
