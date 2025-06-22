import os
from typing import List, Dict

from .scraper import fetch_problems
from .solution_generator import generate_solution_stubs
from .graph_examples import get_graph_by_type, get_graph_info
from .visualizer import animate_search, create_algorithm_explanation
from .performance_analyzer import compare_algorithms, create_performance_report, create_performance_chart

def run_pipeline(problem_limit: int = 100):
    print("1. LeetCode 문제 및 솔루션 스텁 생성")
    problems = fetch_problems(limit=problem_limit)
    print(f"   [LOG] 수집된 문제 수: {len(problems)}")
    if not problems:
        print("   [ERROR] LeetCode 문제 크롤링 실패 또는 0개 크롤링됨")
    else:
        first = problems[0]
        print(f"   첫 번째 문제: {first['title']}")
        print(f"      slug: {first['slug']}")
        print(f"      난이도: {first['difficulty']}")
        print(f"      input_example: {first.get('input_example')}")
    generate_solution_stubs(problems)
    print(f"   [LOG] solutions 폴더 생성 여부: {os.path.exists('solutions')}")
    print(f"   솔루션 스텁이 'solutions/' 폴더에 생성되었습니다.")

    print("\n2. 샘플 그래프 시각화 및 성능 분석")
    graph_types = ['sample', 'tree', 'linear', 'complete', 'cycle', 'grid']
    for graph_type in graph_types:
        print(f"\n- {graph_type.title()} 그래프 처리 시작")
        G = get_graph_by_type(graph_type)
        info = get_graph_info(G)
        print(f"  노드 {info['nodes']}개, 엣지 {info['edges']}개, 연결성={info['is_connected']}")

        for method in ('bfs', 'dfs'):
            save_dir = os.path.join('sample_graphs', f"{graph_type}_{method}")
            os.makedirs(save_dir, exist_ok=True)
            print(f"  {method.upper()} 애니메이션 생성...")
            animate_search(G, start=list(G.nodes())[0], method=method, save_dir=save_dir)
            print(f"  {method.upper()} 설명 파일 생성...")
            create_algorithm_explanation(method, save_dir=save_dir)

        print("  성능 분석 시작...")
        perf_dir = os.path.join('sample_graphs', graph_type)
        os.makedirs(perf_dir, exist_ok=True)
        results = compare_algorithms(G, start=list(G.nodes())[0])
        report_path = create_performance_report(results, info, save_dir=perf_dir)
        chart_path = create_performance_chart(results, save_dir=perf_dir)
        print(f"  성능 보고서: {report_path}")
        print(f"  성능 차트: {chart_path}")
        print(f"- {graph_type.title()} 그래프 처리 완료")

    print("\n파이프라인 실행 완료")

if __name__ == "__main__":
    run_pipeline(problem_limit=100)
