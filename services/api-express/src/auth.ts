import type { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import type { JWTPayload } from "./types.ts";

export function requireAuth(req: Request, res: Response, next: NextFunction) {
  const h = req.header("Authorization") || "";
  if (!h.startsWith("Bearer ")) return res.status(401).json({ error: "missing token" });
  const token = h.slice(7);
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET as string, {
      issuer: process.env.JWT_ISS, audience: process.env.JWT_AUD
    }) as JWTPayload;
    (req as any).user = { id: payload.sub, email: payload.email, name: payload.name };
    return next();
  } catch {
    return res.status(401).json({ error: "invalid token" });
  }
}
