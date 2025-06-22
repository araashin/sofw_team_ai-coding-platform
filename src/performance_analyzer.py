import time
import networkx as nx
from typing import Dict, Any
from collections import deque
import matplotlib.pyplot as plt
import os

def measure_bfs_performance(G: nx.Graph, start: Any) -> Dict:
    start_time = time.perf_counter()
    visited = set()
    queue = deque([start])
    visited.add(start)
    traversal_order = []
    step_count = 0
    while queue:
        current = queue.popleft()
        traversal_order.append(current)
        step_count += 1
        for neighbor in G[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    end_time = time.perf_counter()
    return {
        'algorithm': 'BFS',
        'execution_time': end_time - start_time,
        'steps': step_count,
        'nodes_visited': len(visited),
        'traversal_order': traversal_order,
        'memory_structures': ['Queue']
    }

def measure_dfs_performance(G: nx.Graph, start: Any) -> Dict:
    start_time = time.perf_counter()
    visited = set()
    traversal_order = []
    step_count = [0]
    def dfs_recursive(node):
        visited.add(node)
        traversal_order.append(node)
        step_count[0] += 1
        for neighbor in G[node]:
            if neighbor not in visited:
                dfs_recursive(neighbor)
    dfs_recursive(start)
    end_time = time.perf_counter()
    return {
        'algorithm': 'DFS',
        'execution_time': end_time - start_time,
        'steps': step_count[0],
        'nodes_visited': len(visited),
        'traversal_order': traversal_order,
        'memory_structures': ['Recursion Stack']
    }

def measure_dfs_iterative_performance(G: nx.Graph, start: Any) -> Dict:
    start_time = time.perf_counter()
    visited = set()
    stack = [start]
    traversal_order = []
    step_count = 0
    while stack:
        current = stack.pop()
        if current not in visited:
            visited.add(current)
            traversal_order.append(current)
            step_count += 1
            neighbors = list(G[current])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append(neighbor)
    end_time = time.perf_counter()
    return {
        'algorithm': 'DFS (Iterative)',
        'execution_time': end_time - start_time,
        'steps': step_count,
        'nodes_visited': len(visited),
        'traversal_order': traversal_order,
        'memory_structures': ['Stack']
    }

def compare_algorithms(G: nx.Graph, start: Any) -> Dict:
    results = {}
    results['BFS'] = measure_bfs_performance(G, start)
    results['DFS_Recursive'] = measure_dfs_performance(G, start)
    results['DFS_Iterative'] = measure_dfs_iterative_performance(G, start)
    return results

def create_performance_report(results: Dict, graph_info: Dict, save_dir: str = 'output'):
    os.makedirs(save_dir, exist_ok=True)
    report = f"""
# 알고리즘 성능 분석

- 노드 수: {graph_info['nodes']}
- 엣지 수: {graph_info['edges']}
- 연결성: {'연결됨' if graph_info['is_connected'] else '연결되지 않음'}
- 트리 여부: {'예' if graph_info['is_tree'] else '아니오'}
- 사이클 존재: {graph_info['has_cycles']}
- 지름: {graph_info['diameter']}
- 평균 클러스터링 계수: {graph_info['average_clustering']:.4f}

| 알고리즘 | 실행 시간 (초) | 단계 수 | 방문 노드 수 | 메모리 구조 |
|----------|----------------|---------|--------------|-------------|
"""
    for result in results.values():
        report += f"| {result['algorithm']} | {result['execution_time']:.6f} | {result['steps']} | {result['nodes_visited']} | {', '.join(result['memory_structures'])} |\n"
    report += "\n"
    for result in results.values():
        order_str = ' → '.join(map(str, result['traversal_order']))
        report += f"{result['algorithm']}: {order_str}\n"
    sorted_results = sorted(results.values(), key=lambda x: x['execution_time'])
    fastest = sorted_results[0]['algorithm']
    slowest = sorted_results[-1]['algorithm']
    report += f"\n가장 빠름: {fastest} ({sorted_results[0]['execution_time']:.6f}초)\n"
    report += f"가장 느림: {slowest} ({sorted_results[-1]['execution_time']:.6f}초)\n"
    report += """
- BFS: 레벨 순서, 최단 경로
- DFS (재귀): 깊이 우선, 함수 호출 스택
- DFS (반복): 깊이 우선, 명시적 스택

- 최단 경로 필요: BFS
- 메모리 효율 중요: DFS
- 스택 오버플로우 우려: DFS (반복)
"""
    filename = os.path.join(save_dir, "performance_analysis_report.md")
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(report.strip())
    print(f"   성능 분석 보고서 저장: {filename}")
    return filename

def create_performance_chart(results: Dict, save_dir: str = 'output'):
    os.makedirs(save_dir, exist_ok=True)
    algorithms = [result['algorithm'] for result in results.values()]
    execution_times = [result['execution_time'] * 1000 for result in results.values()]
    steps = [result['steps'] for result in results.values()]
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    bars1 = ax1.bar(algorithms, execution_times, color=['skyblue', 'lightcoral', 'lightgreen'])
    ax1.set_title('알고리즘별 실행 시간 비교', fontsize=14, weight='bold')
    ax1.set_ylabel('실행 시간 (밀리초)')
    ax1.tick_params(axis='x', rotation=45)
    for bar, time_val in zip(bars1, execution_times):
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{time_val:.3f}ms', ha='center', va='bottom')
    bars2 = ax2.bar(algorithms, steps, color=['orange', 'purple', 'brown'])
    ax2.set_title('알고리즘별 실행 단계 수 비교', fontsize=14, weight='bold')
    ax2.set_ylabel('실행 단계 수')
    ax2.tick_params(axis='x', rotation=45)
    for bar, step_val in zip(bars2, steps):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + height*0.01,
                f'{step_val}', ha='center', va='bottom')
    plt.tight_layout()
    chart_path = os.path.join(save_dir, "performance_comparison_chart.png")
    plt.savefig(chart_path, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"   성능 비교 차트 저장: {chart_path}")
    return chart_path
