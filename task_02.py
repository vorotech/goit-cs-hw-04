import os
import logging
from multiprocessing import Process, Queue
from time import time
import pprint


def search_keywords_in_files(file_list, keywords, queue):
    """Search for keywords in files and add results to a queue."""

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

    queue.put(keyword_dict)


def multiprocessing_search(directory, keywords, num_processes=4):
    """Execute a search for keywords in files using multiple processes."""

    # Get list of files in directory
    files = [
        os.path.join(directory, f)
        for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]

    # Split files into chunks for each process
    chunk_size = len(files) // num_processes
    chunks = [files[i : i + chunk_size] for i in range(0, len(files), chunk_size)]

    # Create processes
    processes = []
    queue = Queue()

    for chunk in chunks:
        process = Process(
            target=search_keywords_in_files, args=(chunk, keywords, queue)
        )
        processes.append(process)
        process.start()

    # Wait for all processes to complete
    for process in processes:
        process.join()

    # Combine results from all processes
    combined_results = {keyword: [] for keyword in keywords}
    while not queue.empty():
        result = queue.get()
        for keyword, file_paths in result.items():
            combined_results[keyword].extend(file_paths)

    return combined_results


def main():
    """Main function to demonstrate multiprocessing search."""
    logging.basicConfig(level=logging.DEBUG)

    keywords = ["test", "some", "example"]
    start_time = time()
    results = multiprocessing_search("text_files", keywords, num_processes=4)
    end_time = time()

    print("Multiprocessing Results:")
    pprint.pprint(results, width=80, sort_dicts=False)
    print("Time taken:", end_time - start_time, "seconds")


if __name__ == "__main__":
    main()
