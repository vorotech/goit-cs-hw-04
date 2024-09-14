import os
import logging
from threading import Thread
from time import time
import pprint


def search_keywords_in_files(file_list, keywords, result):
    keyword_dict = {keyword: [] for keyword in keywords}

    for file_path in file_list:
        try:
            with open(file_path, "r") as file:
                content = file.read()
                for keyword in keywords:
                    if keyword in content:
                        keyword_dict[keyword].append(file_path)
        except (FileNotFoundError, PermissionError, IOError) as e:
            logging.error(f"Error processing file {file_path}: {e}")

    result.append(keyword_dict)


def multithreaded_search(directory, keywords, num_threads=4):
    """Execute a search for keywords in files using multiple threads."""

    # Get list of files in directory
    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    # Split files into chunks for each thread
    chunk_size = len(files) // num_threads
    chunks = [files[i : i + chunk_size] for i in range(0, len(files), chunk_size)]

    # Create threads
    threads = []
    results = []

    for chunk in chunks:
        thread = Thread(
            target=search_keywords_in_files, args=(chunk, keywords, results)
        )
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    # Combine results from all threads
    combined_results = {keyword: [] for keyword in keywords}
    for result in results:
        for keyword, file_paths in result.items():
            combined_results[keyword].extend(file_paths)

    return combined_results


def main():
    """Main function to execute the search using multiple threads."""
    logging.basicConfig(level=logging.DEBUG)

    keywords = ["test", "some", "example"]
    start_time = time()
    results = multithreaded_search("text_files", keywords, num_threads=4)
    end_time = time()

    print("Multithreading Results:")
    pprint.pprint(results, width=80, sort_dicts=False)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
