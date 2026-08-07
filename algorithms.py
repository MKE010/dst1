def run_dijkstra(g, s, t):
    dist = {}
    for n in g.nodes:
        dist[n] = float('inf')
    dist[s] = 0
    prev = {}
    for n in g.nodes:
        prev[n] = None
        
    unvis = []
    for n in g.nodes.keys():
        unvis.append(n)

    while len(unvis) > 0:
        curr = None
        m_dist = float('inf')
        for n in unvis:
            if dist[n] < m_dist:
                m_dist = dist[n]
                curr = n

        if curr == None or curr == t:
            break

        unvis.remove(curr)
        for adj, w in g.get_adj(curr):
            if adj in unvis:
                new_d = dist[curr] + w
                if new_d < dist[adj]:
                    dist[adj] = new_d
                    prev[adj] = curr

    p_list = []
    c = t
    while c != None:
        p_list.insert(0, c)
        c = prev[c]
        
    if len(p_list) > 0 and p_list[0] == s:
        return p_list
    else:
        return []

def myBfs(g, s, t):
    v = set()
    q = [[s]]
    if s == t:
        return [s]
        
    while len(q) > 0:
        p = q.pop(0)
        n = p[-1]
        if n not in v:
            for adj, weight_ignore in g.get_adj(n):
                p2 = list(p)
                p2.append(adj)
                if adj == t:
                    return p2
                q.append(p2)
            v.add(n)
    return []