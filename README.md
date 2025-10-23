![Football on Grass](https://images.pexels.com/photos/7154759/pexels-photo-7154759.jpeg?_gl=1*1d4zq10*_ga*MjEzODcwNTY5OC4xNzYxMjYwMDky*_ga_8JE65Q40S6*czE3NjEyNjAwOTIkbzEkZzEkdDE3NjEyNjAxOTUkajI5JGwwJGgw)


# NFL Betting Tracker

NFL Tracker is a Django-based web app that allows users to view and log game-specific notes tied to NFL teams and dates. It fetches real-time team schedules from ESPN’s public API, extracts game metadata (like location, opponent, and score), and enriches each entry with geocoded stadium coordinates and travel distance from the team’s home base. Notes are displayed in a clean, readable list format with intuitive navigation and styling.

This app was designed as a modular starting point for future sports analytics tools. It demonstrates how to scaffold reusable services, integrate external APIs, and deploy a full-stack app with minimal overhead. Future versions could expand into betting insights, player tracking, predictive modeling, or fan engagement features. The architecture encourages iterative learning and collaborative development—ideal for teaching, onboarding, or scaling into more complex domains.


---

# Getting Started

- **Deployed App**: [NFL Tracker on Heroku](https://nfl-betting-tracker-f097951b0a75.herokuapp.com/)
- **Planning Materials**: [Trello Board](https://trello.com/b/L0cI1s9a/betting-tracker-app)


## Attributions

- Python
- Django
- HTML/CSS (Flexbox layout)
- Heroku (deployment)
- Microsoft Copilot — The haversine formula and modular service architecture were scaffolded with support from AI tools to accelerate learning and ensure precision.
- [Django Documentation](https://docs.djangoproject.com/en/stable/) — Core web framework used for routing, models, and views.
- [Google Maps Platform](https://developers.google.com/maps/documentation) — Used for geocoding stadium addresses and enriching game metadata.
- [ESPN Public API](https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams) — Source for team and schedule data.



---

## Next Steps

- **Integrate betting odds and team statistics via API**  
  Pull in real-time betting lines, win probabilities, and team performance metrics to enrich each game entry with contextual data.
- **Aggregate and compute descriptive statistics**  
  Summarize trends across games—such as average margin of victory, travel distances, or performance by weekday—using simple statistical summaries and visualizations.

- **Add filtering and search functionality**  
  Let users filter notes by team, date range, note type, or outcome to quickly surface relevant insights.

- **Improve mobile responsiveness and accessibility**  
  Refine layout and navigation for smaller screens and ensure the app is usable with screen readers and keyboard navigation.

