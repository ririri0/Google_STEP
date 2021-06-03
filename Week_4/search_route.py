import copy


class Queue:
    def __init__(self):
        self.queue = []

    def enq(self, id, route_list):
        data = {'id': id, 'route_list': route_list}
        self.queue.append(data)

    def deq(self):
        if self.queue == {}:
            return False
        else:
            data = self.queue[0]
            del self.queue[0]
            return data

    def isQueue(self):
        if self.queue == []:
            return False
        else:
            return True


def LoadPages(pages):
    with open('data/pages.txt') as f:
        for data in f.read().splitlines():
            page = data.split('\t')
            # page[0]: id, page[1]: title
            pages[page[0]] = page[1]


def LoadLinks(links):
    with open('data/links.txt') as f:
        for data in f.read().splitlines():
            link = data.split('\t')
            # link[0]: id (from), links[1]: id (to)
            if link[0] in links:
                links[link[0]].add(link[1])
            else:
                links[link[0]] = {link[1]}


def InitAccessCount(access_count, pages):
    for id in pages:
        access_count[id] = 0


def SearchID(find_title, pages):
    for id, title in pages.items():
        if title == find_title:
            return id
    
    # Exception
    print(' NOT FOUND ID OF ' + find_title)
    exit(1)


def SearchRoute(start_title, destination_title, pages, links):
    # Search IDs
    start_id = SearchID(start_title, pages)
    destination_id = SearchID(destination_title, pages)

    # Initialize
    bfs_queue = Queue()
    access_count = {}
    InitAccessCount(access_count, pages)

    # Store the Start Word in Queue
    bfs_queue.enq(start_id, [])

    # Serach Route
    while bfs_queue.isQueue():
        deq_data = bfs_queue.deq()
        if access_count[deq_data['id']]:
            pass
        else:
            route_list = copy.copy(deq_data['route_list'])
            route_list.append(deq_data['id'])
            if deq_data['id'] == destination_id:
                return route_list
            else:
                if deq_data['id'] in links:
                    for id in links[deq_data['id']]:
                        bfs_queue.enq(id, route_list)
        access_count[deq_data['id']] += 1

    # Exception
    return 'NOT FOUND ROUTE'


def PrintList(list, pages):
    if isinstance(list, str):
        # Exception
        print(list)
    else:
        print('\nid, title')
        for id in list:
            print('%s %s' % (id, pages[id]))


def main():
    # User Input
    print('Start > ', end="")
    start_title = input()
    print('Destination > ', end="")
    destination_title = input()

    # Load data
    pages = {}
    links = {}
    LoadPages(pages)
    LoadLinks(links)

    # Outout the result
    result = SearchRoute(start_title, destination_title, pages, links)
    PrintList(result, pages)


if __name__ == '__main__':
    main()
