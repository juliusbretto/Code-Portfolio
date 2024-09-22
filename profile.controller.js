import { Router } from "express";
import model from "../model.js";

const router = Router();

router.get("/profile", async (req, res) => {
  const id = req.cookies.sessionCookie;
  const user = model.findUserById(id);
  const stats = await model.getStats(id);
  if (user && stats) {
    res.status(200).json({
      name: user.getName(),
      wins: stats[0],
      losses: stats[1],
      total: stats[2],
    });
  } else {
    res.status(403).end();
  }
});

router.get("/matchhistory", async (req, res) => {
  const id = req.cookies.sessionCookie;
  const user = model.findUserById(id);
  if (user && id) {
    const matches = await model.getUserMatches(id);
    res.status(200).json({
      matches,
      name: user.getName(),
    });
  } else {
    res.status(403).end();
  }
});

router.get("/lobby", (req, res) => {
  const id = req.cookies.sessionCookie;
  const user = model.findUserById(id);
  if (user) {
    res.status(200).json({ name: user.getName() });
  } else {
    res.status(403).end();
  }
});

router.post("/logout", async (req, res) => {
  const id = req.cookies.sessionCookie;
  res.clearCookie("sessionCookie");

  const matchId = req.cookies.match;
  if (matchId) {
    const opponent = model.getOpponent(matchId, id);
    await model.deleteMatchById(matchId, id);
    model.broadcast(`exit/${matchId}`, opponent);
    model.broadcast("cancelmatch", matchId);
    res.clearCookie("match");
  }

  await model.deleteUserById(id);
  res.status(200).end();
});

router.post("/forcelogout", async (req, res) => {
  const id = req.cookies.sessionCookie;
  await model.forceLogout(id);
  res.clearCookie("sessionCookie");
  res.status(200).end();
});

router.post("/activityupdate", async (req, res) => {
  const { active } = req.body;
  const id = req.cookies.sessionCookie;
  const alive = model.activityUpdate(active, id);
  if (alive) {
    res.status(200).end();
  } else {
    res.status(403).end();
  }
});

export default { router };
