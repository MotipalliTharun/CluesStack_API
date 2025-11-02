import { Router } from "express";
import { z } from "zod";
import pkg from "pg";           // CommonJS module → default import
const { Pool } = pkg;
import { requireAuth } from "./auth";

const pool = new Pool({
  host: process.env.POSTGRES_HOST,
  port: +(process.env.POSTGRES_PORT || 5432),
  user: process.env.POSTGRES_USER,
  password: process.env.POSTGRES_PASSWORD,
  database: process.env.POSTGRES_DB
});

const router = Router();

/**
 * @openapi
 * /community/posts:
 *   get:
 *     tags: [community]
 *     summary: List posts
 *     responses:
 *       200:
 *         description: OK
 *   post:
 *     tags: [community]
 *     summary: Create post
 *     security: [{ bearerAuth: [] }]
 *     requestBody:
 *       required: true
 *     responses:
 *       201: { description: Created }
 */
router.get("/posts", async (_req, res) => {
  await pool.query(`
    CREATE TABLE IF NOT EXISTS community_posts (
      id text primary key,
      author_id text,
      title text,
      body text,
      created_at timestamptz default now()
    );
  `);
  const result = await pool.query(
    "SELECT id, author_id, title, body, created_at FROM community_posts ORDER BY created_at DESC LIMIT 50;"
  );
  res.json(result.rows);
});

router.post("/posts", requireAuth, async (req, res) => {
  const schema = z.object({ title: z.string().min(1), body: z.string().min(1) });
  const parsed = schema.safeParse(req.body);
  if (!parsed.success) return res.status(422).json({ error: parsed.error.flatten() });
  const id = "post_" + Math.random().toString(36).slice(2, 10);
  await pool.query(
    "INSERT INTO community_posts (id, author_id, title, body) VALUES ($1,$2,$3,$4)",
    [id, (req as any).user.id, parsed.data.title, parsed.data.body]
  );
  res.status(201).json({ id, ...parsed.data, author_id: (req as any).user.id });
});

export default router;
