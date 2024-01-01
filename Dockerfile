FROM selenium/hub:latest

ENV GRID_MAX_SESSION 16
ENV GRID_BROWSER_TIMEOUT 3000
ENV GRID_TIMEOUT 3000

EXPOSE 4444

CMD ["start"]
