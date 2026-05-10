from abc import ABC, abstractmethod
from typing import List
import json
import asyncio

class SearchEngine(ABC):
    @abstractmethod
    async def asearch(self, keywords: str | List[str]) -> list:
        NotImplementedError("Async search not implemented for this engine")
    @abstractmethod
    async def asearch_by_id(self, id: str) -> dict:
        NotImplementedError("Async search by ID not implemented for this engine")
    


class IssueSearchEngine(SearchEngine):
    def __init__(self):
        self._data = None

        with open('.data/issue_samples.json', 'r') as f:
            self._data = json.load(f)

    async def asearch_by_id(self, id: str) -> dict:
        asyncio.sleep(0.5)  # Simulate search delay
        for issue in self._data:
            if issue['issue_id'] == id:
                return issue
        return None

    
    async def asearch(self, keywords: str | List[str]) -> list:
        asyncio.sleep(1.5)  # Simulate search delay
        if isinstance(keywords, str):
            keywords = [keywords]

        results = []
        for keyword in keywords:
            for issue in self._data:
                if keyword.lower() in issue['keywords']:
                    results.append(issue)
        return results
    
class DiscussionSearchEngine(SearchEngine):
    def __init__(self):
        self._data = None

        with open('.data/issue_discussions_samples.json', 'r') as f:
            self._data = json.load(f)

    async def asearch_by_id(self, id: str) -> dict:
        asyncio.sleep(0.5)  # Simulate search delay
        for discussion in self._data:
            if discussion['discussion_id'] == id:
                return discussion
        return None

    async def asearch(self, keywords: str | List[str]) -> list:
        asyncio.sleep(0.5)  # Simulate search delay
        if isinstance(keywords, str):
            keywords = [keywords]

        results = []
        for keyword in keywords:
            for log in self._data:
                if keyword.lower() in log['body'].lower():
                    results.append(log)
        return results
    
