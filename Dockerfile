FROM nginx:stable-alpine

ENV PORT=8080

COPY deploy/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY index.html World_Models_TechMap.html graph-data.js paper-data.js cytoscape.min.js layout-base.js cose-base.js cytoscape-fcose.js /usr/share/nginx/html/

EXPOSE 8080
