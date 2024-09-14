import os
from faker import Faker


def generate_readable_text_files(num_files, directory, num_lines=100):
    """Generate a specified number of readable text files in a directory."""
    os.makedirs(directory, exist_ok=True)
    fake = Faker()

    for i in range(num_files):
        file_path = os.path.join(directory, f"readable_file_{i}.txt")
        with open(file_path, "w", newline="") as file:
            for _ in range(num_lines):
                # Generate a random sentence using Faker
                sentence = fake.sentence(nb_words=10)
                file.write(sentence + "\n")


def main():
    generate_readable_text_files(num_files=100, directory="text_files", num_lines=1000)


if __name__ == "__main__":
    main()
