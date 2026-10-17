from functions.get_file_content import get_file_content

result = get_file_content("calculator", "lorem.txt")

#Should be a bit over 10000/MAX_CHARS since it includes truncate message
print(f"lorem.txt length: {len(result)}")

#True if the word truncated appears in result
print(f"lorem.txt truncated: {'truncated' in result}")

print(get_file_content("calculator", "main.py"))
print(get_file_content("calculator", "pkg/calculator.py"))
#Returns an error
print(get_file_content("calculator", "/bin/cat"))
print(get_file_content("calculator", "pkg/does_not_exist.py"))


