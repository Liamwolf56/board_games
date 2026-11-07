import json
import os

class CampaignProgressManager:
    def __init__(self, save_filename="story/progress.json"):
        # Resolve path relative to the project root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.save_path = os.path.join(base_dir, save_filename)
        self.data = self.load_progress()

    def default_progress(self):
        """Returns the default initial state for a brand new campaign run."""
        return {
            "player_name": "Challenger",
            "campaign_order": [],
            "current_stage_idx": 0,
            "high_score": 0,
            "kings_defeated_this_run": 0,
            "run_active": False
        }

    def load_progress(self):
        """Loads campaign progress from disk, falling back to defaults if missing or corrupted."""
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, "r") as f:
                    data = json.load(f)
                    # Validate required keys exist
                    required_keys = ["player_name", "campaign_order", "current_stage_idx", "high_score"]
                    if all(k in data for k in required_keys):
                        return data
            except Exception:
                pass
        return self.default_progress()

    def save_progress(self, player_name, campaign_order, current_stage_idx, high_score):
        """Persists the current campaign run state to JSON."""
        self.data = {
            "player_name": player_name,
            "campaign_order": campaign_order,
            "current_stage_idx": current_stage_idx,
            "high_score": max(high_score, current_stage_idx),
            "kings_defeated_this_run": current_stage_idx,
            "run_active": current_stage_idx < len(campaign_order)
        }
        
        # Ensure target directory exists
        os.makedirs(os.path.dirname(os.path.abspath(self.save_path)), exist_ok=True)
        with open(self.save_path, "w") as f:
            json.dump(self.data, f, indent=4)

    def advance_stage(self):
        """Advances the player to the next stage upon defeating a king."""
        self.data["current_stage_idx"] += 1
        self.data["kings_defeated_this_run"] = self.data["current_stage_idx"]
        
        if self.data["current_stage_idx"] > self.data["high_score"]:
            self.data["high_score"] = self.data["current_stage_idx"]
            
        self.save_progress(
            self.data["player_name"],
            self.data["campaign_order"],
            self.data["current_stage_idx"],
            self.data["high_score"]
        )

    def reset_run(self, player_name, campaign_order):
        """Resets the current run back to Stage 1 while preserving high scores."""
        current_high = max(self.data.get("high_score", 0), self.data.get("current_stage_idx", 0))
        self.save_progress(player_name, campaign_order, 0, current_high)

    def get_summary(self):
        """Returns a quick status dictionary of the current campaign."""
        return {
            "name": self.data.get("player_name", "Challenger"),
            "stage": self.data.get("current_stage_idx", 0),
            "total_stages": len(self.data.get("campaign_order", [])),
            "high_score": self.data.get("high_score", 0)
        }
