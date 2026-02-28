import os

def main():
    try:
        with open("README.md", "r", encoding="utf-8") as rf:
            readme_content = rf.read()
            
        with open("PROJECT_DOCUMENTATION.txt", "a", encoding="utf-8") as df:
            df.write("\n\n7. PROJECT README & SETUP INSTRUCTIONS\n")
            df.write("======================================\n\n")
            df.write(readme_content)
            
        print("Successfully appended README.md to PROJECT_DOCUMENTATION.txt")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
