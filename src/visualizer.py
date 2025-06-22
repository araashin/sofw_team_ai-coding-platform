import os
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from typing import Any

import matplotlib
matplotlib.rc('font', family='Malgun Gothic')
matplotlib.rcParams['axes.unicode_minus'] = False

def animate_search(G: nx.Graph, start: Any, method: str = 'bfs', save_dir: str = 'output'):
    print(f"    {method.upper()} 탐색 순서 계산 중...")
    if method == 'bfs':
        traversal = list(nx.bfs_tree(G, start))
    else:
        traversal = list(nx.dfs_tree(G, start))
    print(f"    탐색 순서: {' → '.join(map(str, traversal))}")
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(12, 9))
    visited = []

    def update(frame):
        ax.clear()
        if frame < len(traversal):
            visited.append(traversal[frame])
        node_colors = []
        for node in G.nodes():
            if node in visited:
                if node == visited[-1]:
                    node_colors.append('red')
                else:
                    node_colors.append('lightcoral')
            else:
                node_colors.append('lightgrey')
        edge_colors = []
        for edge in G.edges():
            if edge[0] in visited and edge[1] in visited:
                edge_colors.append('red')
            else:
                edge_colors.append('grey')
        nx.draw(G, pos, with_labels=True, node_color=node_colors,
                edge_color=edge_colors, node_size=1000,
                font_size=18, font_weight='bold', font_color='white',
                width=2, ax=ax)
        current = visited[-1] if visited else start
        step = f"단계 {len(visited)}/{len(traversal)}" if visited else "시작"
        ax.set_title(
            f"{method.upper()} 탐색 시각화\n{step} - 현재 노드: {current}\n"
            f"방문 순서: {' → '.join(map(str, visited)) if visited else '시작 대기'}",
            fontsize=16
        )
        from matplotlib.patches import Patch
        legend = [
            Patch(facecolor='red', label='현재'),
            Patch(facecolor='lightcoral', label='방문 완료'),
            Patch(facecolor='lightgrey', label='미방문')
        ]
        ax.legend(handles=legend, loc='upper left', fontsize=12)
        ax.text(0.02, 0.02, get_algorithm_info(method), transform=ax.transAxes,
                fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

    print("    애니메이션 프레임 생성 중...")
    ani = animation.FuncAnimation(fig, update, frames=len(traversal)+2, interval=2000, repeat=True)
    os.makedirs(save_dir, exist_ok=True)
    gif_path = os.path.join(save_dir, f"{method}_animation.gif")
    try:
        print(f"    GIF 애니메이션 저장 중...")
        ani.save(gif_path, writer='pillow', fps=0.5)
        print(f"    저장 완료: {gif_path}")
        png_path = os.path.join(save_dir, f"{method}_final_state.png")
        update(len(traversal)-1)
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        print(f"    저장 완료: {png_path}")
    except Exception as e:
        print(f"    애니메이션 저장 실패: {e}")
        steps_dir = os.path.join(save_dir, f"{method}_steps")
        os.makedirs(steps_dir, exist_ok=True)
        for i in range(len(traversal)):
            update(i)
            node = traversal[i]
            step_file = os.path.join(steps_dir, f"step_{i+1:02d}_{node}.png")
            plt.savefig(step_file, dpi=200, bbox_inches='tight')
        print(f"    단계별 이미지 저장: {steps_dir}")
    plt.close()

def get_algorithm_info(method: str) -> str:
    if method == 'bfs':
        return "BFS: 큐 사용, 너비 우선"
    return "DFS: 스택 사용, 깊이 우선"

def create_algorithm_explanation(method: str, save_dir: str = 'output'):
    os.makedirs(save_dir, exist_ok=True)
    if method == 'bfs':
        explanation = """
# BFS
1. 큐로 레벨별 탐색
2. 최단 경로 보장
"""
    else:
        explanation = """
# DFS
1. 스택 또는 재귀로 깊이 탐색
2. 메모리 효율
"""
    path = os.path.join(save_dir, f"{method}_explanation.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(explanation.strip())
    print(f"    설명 파일 저장: {path}")

def create_comparison_document(save_dir: str = 'output'):
    os.makedirs(save_dir, exist_ok=True)
    comparison = ""
    path = os.path.join(save_dir, "bfs_vs_dfs_comparison.md")
    with open(path, 'w', encoding='utf-8') as f:
        f.write(comparison)
    print(f"    비교 문서 저장: {path}")
