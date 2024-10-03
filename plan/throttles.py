from rest_framework.throttling import SimpleRateThrottle

class LowVoteThrottle(SimpleRateThrottle):
    scope = 'low_vote'

    def get_cache_key(self, request, view):
        vote_value = request.data.get('vote')
        plan_id = view.kwargs.get('plan_id')

        if vote_value not in [1, 2] and not plan_id:
            return None

        return f"throttle_low_plan_vote_{plan_id}_{vote_value}"

    
class HighVoteThrottle(SimpleRateThrottle):
    scope = 'high_vote'

    def get_cache_key(self, request, view):
        vote_value = request.data.get('vote')
        plan_id = view.kwargs.get('plan_id')

        if vote_value not in [4, 5] and not plan_id:
            return None

        return f"throttle_high_plan_vote_{plan_id}_{vote_value}"