import sys
import collections

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
        print("Finished reading %s" % links_file)
        print()


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()

    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()

    def find_link(self, page_name):
        #This will return the page id given its name, so A returns 1
        for key,val in self.titles.items():
            if val == page_name:
                return key

    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        if start == goal: return start
        q = collections.deque()
        #Queue: title : "A", id: 1, path, distance
        q.append([start, self.find_link(start), [str(start)], 0])

        visited = set()
        visited.add(start)

        while q:
            page, page_id, path, distance = q.popleft()
            if page == goal:
                print("".join(path), "with a distance of", distance)
                # return path + ["-->", str(goal)]
            
            for node in self.links[page_id]:
                if node not in visited:
                    visited.add(node)
                    q.append((self.titles[node], node, path + [" --> "] + [self.titles[node]], distance + 1))

        return "No Path Found!"
    
    def check_convergence(self, old, new, threshold):
        # sum = 0
        # for page in old:
        #     sum += (old[page] - new[page]) ** 2
        # if sum > threshold:
        #     print(sum, "FALSE")
        #     return False
        # return True

        s = sum((old[page]-new[page])**2 for page in old)
        if s > threshold:
            return False
        return True
    
    def page_rank(self, max_iter=100):
        num_pages = len(self.titles)
        threshold = 0.01
        #Step 1: Give all nodes an initial value of 1.0
        pagerank = {i:1.0 for i in self.titles.values()}
        convergence = False
        num_outgoing_links = {i:0 for i in self.titles.values()}
        # no_links = []
            
        #create dictionary to store number of outgoing links for each page
        for page, linked_p in self.links.items():
            num_outgoing_links[page] = len(linked_p)
            # if num_outgoing_links[page] == 0:
            #     no_links.append(self.titles[page])
        
        iterations = 0
        while not convergence and iterations < max_iter:
        # store new_pageranks
            new_pagerank = {i:0.0 for i in self.titles.values()}
            total = 0
            
            #Step 2 and 3: Find each node's page_rank and distriubute it to adj pages
            for page, linked_page in self.links.items():
                if num_outgoing_links[page] > 0:
                    score = pagerank[self.titles[page]] / num_outgoing_links[page]
                for p in linked_page:
                    new_pagerank[self.titles[p]] += score
                else:
                    #collect scores from all nodes with no linkes
                    total += pagerank[self.titles[page]]
            
            #distribute values of all nodes with no links to nodes with links
            if total > 0:
                distribute_val = total / num_pages
                for page in new_pagerank:
                    new_pagerank[page] += distribute_val
            
            # #check for convergence
            convergence = self.check_convergence(pagerank, new_pagerank, threshold)
            # #update pagerank everytime
            pagerank = new_pagerank
            iterations += 1

        return pagerank  

    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
       pagerank = self.page_rank()
       pagerank = sorted(pagerank.items(), key = lambda x: -x[1])
       
       print("The Top 10 Most Popular Pages:")
       for i in range(10):
           print(i+1, pagerank[i][0])
    
    def find_least_popular_pages(self):
        pagerank = self.page_rank()
        pagerank = sorted(pagerank.items(), key = lambda x: x[1])
       
        print("The Top 10 Least Popular Pages:")
        for i in range(10):
           print(i+1, pagerank[i][0])
           
    # Do something more interesting!! 
    def find_something_more_interesting(self, start):
        #FIND NODES FURTHEST FROM START
        distances = {page: float("inf") for page in self.titles.values()}
        distances[start] = 0
        q = collections.deque([start])
        visited = set()
        visited.add(start)

        while q:
            page = q.popleft()
            print(page)
            for linked_page in self.links[self.find_link(page)]:
                if distances[self.titles[linked_page]] == float("inf") and self.titles[linked_page] not in visited:
                    distances[self.titles[linked_page]] = distances[page] + 1
                    q.append(self.titles[linked_page])
                    visited.add(self.titles[linked_page])

        farthest = max(distances, key = distances.get)
        farthest_disntace = distances[farthest]
        return farthest, farthest_disntace
    
    def find_furthest(self):
        longest_distnace = 0 
        for page in self.titles.values():
            self.find_something_more_interesting(page)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    # wikipedia.find_longest_titles()
    # wikipedia.find_most_linked_pages()
    # wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
    wikipedia.find_least_popular_pages()
    # print(wikipedia.find_something_more_interesting("渋谷"))
    # wikipedia.find_furthest()