import requests

class Commands:

    def __init__(self, SEASON, API_BASE, HEADERS):
        self.SEASON = SEASON
        self.API_BASE = API_BASE
        self.HEADERS = HEADERS

    def get_team_data(self, team, season):
        return requests.get(f"{self.API_BASE}/team/{team}/results/{season}", headers=self.HEADERS)

    # Find a team's average OPR
    def avg_opr(self, team_event_data):
        if len(team_event_data.json()) == 0:
            return 0
        return sum(i['opr'] for i in team_event_data.json()) / len(team_event_data.json())


    def help(self):
        print("help - Shows this message.")
        print("exit - Exits the program.")
        print("versus - Simulates a hypothetical match.")

    def exit(self):
        print("Exiting...")
        exit()

    def versus(self):
        print("Enter Red Alliance Team Numbers (separated by spaces):")
        red = input(">>> ").split(" ")
        print("Enter Blue Alliance Team Numbers (separated by spaces):")
        blue = input(">>> ").split(" ")
        print("Simulating Match... ", end="", flush=True)
        # Get Sum of OPRs
        red_opr = sum(self.avg_opr(self.get_team_data(team, self.SEASON)) for team in red)
        blue_opr = sum(self.avg_opr(self.get_team_data(team, self.SEASON)) for team in blue)
        # Calculate Odds
        red_odds = red_opr / (red_opr + blue_opr)
        blue_odds = blue_opr / (red_opr + blue_opr)
        # Print Results
        print("Done!")
        if red_odds > blue_odds:
            print(f"Red Alliance wins with a ≈{round(red_odds * 100, 2)}% chance of winning and an estimated score of {round(red_opr)} to {round(blue_opr)}.")
        elif blue_odds > red_odds:
            print(f"Blue Alliance wins with a ≈{round(blue_odds * 100, 2)}% chance of winning and an estimated score of {round(blue_opr)} to {round(red_opr)}.")