import requests
import json
from collections import defaultdict

class GitHubAnalyzer:
    def __init__(self, github_token=None):
        self.github_token = github_token
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if self.github_token:
            self.headers["Authorization"] = f"token {self.github_token}"

    def get_user_repositories(self, username):
        """Fetches public repositories for a given GitHub user."""
        repos = []
        page = 1
        while True:
            url = f"https://api.github.com/users/{username}/repos?page={page}&per_page=100"
            print(f"Fetching repositories for {username}, page {page}...")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if not data:
                    break  # No more repositories
                repos.extend(data)
                page += 1
            else:
                print(f"Error fetching repositories: {response.status_code} - {response.text}")
                return None
        return repos

    def get_repository_languages(self, owner, repo_name):
        """Fetches language breakdown for a specific repository."""
        url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        else:
            # print(f"Error fetching languages for {owner}/{repo_name}: {response.status_code} - {response.text}")
            return {}

    def get_user_commit_activity(self, username):
        """
        A simplified way to get some activity.
        For detailed analysis, you'd need to iterate through commits.
        """
        # This is very basic. A real analysis would involve cloning repos
        # or using the events API which has rate limits and complexity.
        # For simplicity, we'll just look at repos and their languages.
        repos = self.get_user_repositories(username)
        if not repos:
            return {}

        language_usage = defaultdict(int)
        topics = defaultdict(int)
        star_count = 0
        fork_count = 0

        for repo in repos:
            # Aggregate languages
            repo_languages = self.get_repository_languages(username, repo['name'])
            for lang, bytes_of_code in repo_languages.items():
                language_usage[lang] += bytes_of_code

            # Aggregate topics (if available and relevant to vulnerabilities)
            for topic in repo.get('topics', []):
                topics[topic] += 1

            star_count += repo.get('stargazers_count', 0)
            fork_count += repo.get('forks_count', 0)

        # Convert bytes to percentage for languages
        total_bytes = sum(language_usage.values())
        language_percentages = {lang: (bytes_ / total_bytes * 100) for lang, bytes_ in language_usage.items()} if total_bytes > 0 else {}

        return {
            "language_percentages": language_percentages,
            "topics": dict(topics),
            "total_stars": star_count,
            "total_forks": fork_count,
            "repo_count": len(repos)
        }


    def recommend_vulnerability_problems(self, username):
        """
        Analyzes user's GitHub activity to recommend vulnerability-related problems.
        This is a highly simplified logic.
        """
        activity = self.get_user_commit_activity(username)
        if not activity:
            return ["Could not retrieve GitHub activity for recommendation."]

        recommendations = []
        language_percentages = activity.get("language_percentages", {})
        topics = activity.get("topics", {})

        print(f"\nAnalyzing activity for {username}:")
        print(f"Languages: {language_percentages}")
        print(f"Topics: {topics}")

        # --- Simple Rule-Based Recommendation Logic ---

        # 1. Based on dominant languages
        if "Python" in language_percentages and language_percentages["Python"] > 50:
            recommendations.append("Python security best practices (e.g., SQL injection prevention, XSS in web apps).")
            recommendations.append("Understanding common Python vulnerabilities (e.g., pickle deserialization issues).")
        if "JavaScript" in language_percentages and language_percentages["JavaScript"] > 50:
            recommendations.append("JavaScript client-side security (e.g., DOM-based XSS, insecure APIs).")
            recommendations.append("Node.js security (e.g., dependency vulnerabilities, path traversal).")
        if "Java" in language_percentages and language_percentages["Java"] > 50:
            recommendations.append("Java security (e.g., deserialization, XXE, insecure JNDI).")
            recommendations.append("Spring Security configurations and common pitfalls.")

        # 2. Based on specific topics found in repositories (hypothetical mapping)
        if "web" in topics or "backend" in topics or "frontend" in topics:
            recommendations.append("Web application security fundamentals (OWASP Top 10).")
        if "data-science" in topics or "ml" in topics:
            recommendations.append("Security in machine learning pipelines (e.g., data poisoning, model evasion).")
        if "api" in topics:
            recommendations.append("API security design principles (e.g., OAuth, API Gateway security).")

        # 3. If very few repositories or low activity, suggest fundamentals
        if activity.get("repo_count", 0) < 5 or (activity.get("total_stars", 0) + activity.get("total_forks", 0)) < 10:
            recommendations.append("Fundamental secure coding principles.")
            recommendations.append("Introduction to common attack vectors.")

        if not recommendations:
            recommendations.append("No specific vulnerability patterns detected. Consider exploring general secure coding practices.")

        return list(set(recommendations)) # Remove duplicates

# Example Usage:
if __name__ == "__main__":
    GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN" # Replace with your actual token
    # Get a token from: https://github.com/settings/tokens (select 'repo' scope for private repos)

    analyzer = GitHubAnalyzer(github_token=GITHUB_TOKEN)
    target_username = "octocat" # Replace with a GitHub username you want to analyze

    print(f"Analyzing GitHub activity for: {target_username}")
    recommended_problems = analyzer.recommend_vulnerability_problems(target_username)

    if recommended_problems:
        print(f"\nRecommended Vulnerability Problems for {target_username}:")
        for problem in recommended_problems:
            print(f"- {problem}")
    else:
        print("No recommendations could be generated.")