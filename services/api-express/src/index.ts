import "dotenv/config";
import express from "express";
import helmet from "helmet";
import cors from "cors";
import communityRouter from "./community.js";
import swaggerUi from "swagger-ui-express";
import swaggerJSDoc from "swagger-jsdoc";

const app = express();
app.use(helmet());
app.use(cors());
app.use(express.json());

// Simple health
app.get("/healthz", (_req, res) => res.json({ status: "ok" }));

// Community routes
app.use("/community", communityRouter);

// OpenAPI (generated from JSDoc)
const swaggerSpec = swaggerJSDoc({
  definition: {
    openapi: "3.1.0",
    info: { title: "CluesStack (Express)", version: "1.0.0" },
    components: {
      securitySchemes: {
        bearerAuth: { type: "http", scheme: "bearer", bearerFormat: "JWT" }
      }
    },
    servers: [{ url: "http://localhost:" + (process.env.EXPRESS_PORT || 4000) }]
  },
  apis: ["./src/**/*.ts"]
});

app.use("/docs", swaggerUi.serve, swaggerUi.setup(swaggerSpec));
app.get("/openapi.json", (_req, res) => res.json(swaggerSpec));

app.listen(process.env.EXPRESS_PORT || 4000, () =>
  console.log("Express on :", process.env.EXPRESS_PORT || 4000)
);
