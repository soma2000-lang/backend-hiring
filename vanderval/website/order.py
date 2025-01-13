
from django.db.models import Count
from vanderval.website.models import Site, Jobs
from typing import Dict, List
from enum import Enum

class TaskPriority(Enum):
    TASK1 = ("task1", 5)
    TASK2 = ("task2", 4)
    TASK3 = ("task3", 3)
    TASK4 = ("task4", 2)
    TASK5 = ("task5", 1)

    @classmethod
    def get_weights(cls) -> Dict[str, int]:
        return {task.value[0]: task.value[1] for task in cls}

class SitePrioritizer:
    def __init__(self):
        self._capacity_weights = {
            Site.RECORD_CAPACITY_HIGH: 3,
            Site.RECORD_CAPACITY_MEDIUM: 2,
            Site.RECORD_CAPACITY_LOW: 1,
        }
        self._task_weights = TaskPriority.get_weights()

    def _get_site_capacity_score(self, site: Site) -> int:
        """Calculate score based on site's record capacity."""
        return self._capacity_weights.get(site.record_capacity, 0)

    def _get_pending_tasks_score(self, site: Site) -> int:
        """Calculate score based on pending tasks and their priorities."""
        pending_tasks = Jobs.objects.filter(
            site=site,
            status="pending"
        ).values("task").annotate(
            count=Count("id")
        ).values_list("task", "count")

        return sum(
            self._task_weights.get(task, 0) * count
            for task, count in pending_tasks
        )

    def calculate_priority_score(self, site: Site) -> int:
        """Calculate total priority score for a site."""
        try:
            capacity_score = self._get_site_capacity_score(site)
            task_score = self._get_pending_tasks_score(site)
            return capacity_score + task_score
        except Exception:

            return 0

    def get_prioritized_sites(self, limit: int = None) -> List[Site]:
       
        sites = Site.objects.all()
        sites_with_scores = [
            (site, self.calculate_priority_score(site))
            for site in sites
        ]
        sorted_sites = sorted(
            sites_with_scores,
            key=lambda x: x[1],
            reverse=True
        )
        
    
        prioritized_sites = [site for site, _ in sorted_sites]
        
        return prioritized_sites[:limit] if limit else prioritized_sites

def prioritize_sites(limit: int = None) -> List[Site]:
    """
    Get a prioritized list of sites.
    Args:
        limit: Optional maximum number of sites to return
    Returns:
        List of sites ordered by priority
    """
    prioritizer = SitePrioritizer()
    return prioritizer.get_prioritized_sites(limit=limit)