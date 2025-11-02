import fs from "node:fs";
import path from "node:path";

const fastapi = JSON.parse(fs.readFileSync(path.resolve("openapi/fastapi.json"), "utf8"));
const express = JSON.parse(fs.readFileSync(path.resolve("openapi/express.json"), "utf8"));

const merged = {
  openapi: "3.1.0",
  info: { title: "CluesStack API (merged)", version: "1.0.0" },
  servers: [
    { url: "http://localhost:8000", description: "FastAPI" },
    { url: "http://localhost:4000", description: "Express" }
  ],
  components: {
    securitySchemes: {
      bearerAuth: { type: "http", scheme: "bearer", bearerFormat: "JWT" }
    }
  },
  paths: {
    ...fastapi.paths,
    ...express.paths
  }
};

fs.writeFileSync(path.resolve("openapi/merged.json"), JSON.stringify(merged, null, 2));
console.log("Merged → openapi/merged.json");
