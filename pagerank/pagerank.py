import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    if page in corpus:#Check if page has outgoing links
        page_probability = {}#Dictionary that assign key values
        num_links = len(corpus[page])
        for linked_page in corpus[page]:#Given a random page assign it probability
            page_probability[linked_page] = damping_factor / num_links#If it has outgoing links
    else:
        total_pages = len(corpus)#Get how many pages have in the corpus
        total_page_prob = {}#Dictionary that assing key values
        for p in corpus:#A key(page) in corpus
            total_page_prob[p] = (1 - damping_factor) / total_pages#If it didnt have outgoing links

    if page in corpus:
        return page_probability
    else:
        return total_page_prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    rank_page = {page_name: 0 for page_name in corpus}

    #First sample
    current_sample = random.choice(list(rank_page))
    rank_page[current_sample] += 1

    #Remaining samples (n-1 samples now)
    for i in range(0, n-1):
        tran_prob = transition_model(corpus, current_sample,damping_factor)#Pass the previous sample into your transition_model function
        # Pick next page based on the transition model probabilities:
        rand_val = random.random()#Generates a random value between 0 and 1
        total_prob = 0

        for page_name, probability in tran_prob.items():#Iterates over each page and its corresponding probability
            total_prob += probability
            if rand_val <= total_prob:#If the random value <= to the running total, it selects as the next page and break.
                current_sample = page_name
                break

        rank_page[current_sample] += 1

    # Normalise visits using sample number:
    page_ranks = {page_name: (visit_num/n) for page_name, visit_num in rank_page.items()}

    return page_ranks



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)#Get the total number of pages in the corpus
    #Assigning a value / Inside the corpus are the pages(keys) and they will receive a value of 1/N
    current_rank = 1 / num_pages
    rank_of_page = {page_name: current_rank for page_name in corpus}#Dictionary
    #Repeatedly calculate new rank values based on all of the current rank values untill new_rank no longer differing more than 0.001
    while True:
        max_rank_change = 0
        new_rank = {page_name: None for page_name in corpus}

        for page_name in corpus:
            # Calculate the new rank for the current page using the transition model
            new_rank[page_name] = (1 - damping_factor) / num_pages  # Initialize with the second term
            for linking_page, links in corpus.items():
                if page_name in links:
                    num_links = len(links)
                    new_rank[page_name] += damping_factor * (rank_of_page[linking_page] / num_links)

            # Calculate the change in rank for the current page
            rank_change = abs(rank_of_page[page_name] - new_rank[page_name])
            max_rank_change = max(max_rank_change, rank_change)  # Update the maximum change

        # Update all ranks with the newly calculated ranks
        rank_of_page = new_rank.copy()

        # Check for convergence (max rank change for all pages)
        if max_rank_change < 0.001:
            break

    return rank_of_page


if __name__ == "__main__":
    main()
