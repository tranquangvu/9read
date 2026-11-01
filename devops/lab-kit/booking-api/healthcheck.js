// Container HEALTHCHECK for a distroless image (no shell, no curl): exits 0 when /healthz answers 200.
import http from "node:http";
http.get({ host: "127.0.0.1", port: process.env.PORT || 8080, path: "/healthz", timeout: 3000 },
  (r) => process.exit(r.statusCode === 200 ? 0 : 1)).on("error", () => process.exit(1));
