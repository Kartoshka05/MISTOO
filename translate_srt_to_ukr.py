import openai
import os

openai.api_key = os.environ.get('OPENAI_API_KEY')

def translate_srt_with_openai(file_path):
    messages = [{"role": "system", "content": "translate to ukrainian and reword to sound better."}]

    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    translated_lines = []
    for line in lines:
        if '-->' not in line and not line.strip().isdigit():
            messages.append({"role": "user", "content": line})
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            translated_line = response.choices[0].message.content
            translated_lines.append(translated_line)
        else:
            translated_lines.append(line)

    base_path, filename = os.path.split(file_path)
    base_filename = os.path.splitext(filename)[0]
    translated_filename = f"{base_filename}_ukr.srt"
    translated_file_path = os.path.join(base_path, translated_filename)

    with open(translated_file_path, 'w', encoding='utf-8') as file:
        file.writelines(translated_lines)

if __name__ == '__main__':
    srt_file_path = input("Введите путь к файлу .srt: ")
    translate_srt_with_openai(srt_file_path)
