[out:json][timeout:90];
(
  relation["boundary"="traffic_zone"](36,6,47.5,19);
  relation["boundary"="low_emission_zone"](36,6,47.5,19);
  relation["name"~"ZTL",i](36,6,47.5,19);
  relation["name"~"^Area [BC]$"](45.3,9.0,45.6,9.35);
  way["name"~"^ZTL",i](36,6,47.5,19);
);
out tags center;
