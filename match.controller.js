import { Router } from "express";
import xss from "xss"; // Import the "xss" module
import model from "../model.js";

const router = Router();

router.get("/matches", (req, res) => {
  const matches = model.getMatches();
  res.status(200).json({ matches });
});

router.post("/newmatch", async (req, res) => {
  const id = req.cookies.sessionCookie;
  const { colour } = req.body;
  const matchId = await model.createMatch(id, colour);
  if (matchId) {
    model.broadcast("newmatch", [
      colour,
      model.findUserById(id).getName(),
      matchId,
    ]);
    res.cookie("match", matchId).status(200).end();
  } else {
    res.status(403).end();
  }
});

router.post("/joinmatch", async (req, res) => {
  const { matchId } = req.body;
  const cleanMatchId = xss(matchId);
  const id = req.cookies.sessionCookie;
  const joined = await model.joinMatch(cleanMatchId, id);

  if (matchId && joined) {
    model.broadcast(`startmatch/${matchId}`, "");
    model.broadcast("joined", matchId);
    res.cookie("match", matchId).status(200).end();
  } else {
    res.status(403).end();
  }
});

router.post("/movepiece", async (req, res) => {
  const { x1, y1, x2, y2 } = req.body;
  const matchId = req.cookies.match;

  const moved = await model.move(matchId, x1, y1, x2, y2);
  if (moved) {
    model.broadcast(`moved/${matchId}`, "");
    const win = await model.checkWin(matchId);
    if (win) {
      const id = req.cookies.sessionCookie;
      model.broadcast(`win/${matchId}`, model.findUserById(id).getName());
    }
  }
  res.status(200).json({ moved, msg: model.getMsg(matchId) });
});

router.get("/match", (req, res) => {
  const matchId = req.cookies.match;
  const id = req.cookies.sessionCookie;
  if (matchId) {
    res.status(200).json({
      gameboard: model.getGameboard(matchId),
      msg: model.getMsg(matchId),
      turn: model.getTurn(matchId, id),
    });
  } else {
    res.status(403).end();
  }
});

router.get("/setupmatch", (req, res) => {
  const matchId = req.cookies.match;
  const id = req.cookies.sessionCookie;
  if (matchId) {
    res.status(200).json({
      black: model.getColour(matchId, id),
      opponent: model.getOpponent(matchId, id),
      matchId,
    });
  } else {
    res.status(403).end();
  }
});

router.get("/exitgame", async (req, res) => {
  const matchId = req.cookies.match;
  const id = req.cookies.sessionCookie;
  if (matchId && id) {
    if (model.getMatchById(matchId)) {
      const opponent = model.getOpponent(matchId, id);
      await model.deleteMatchById(matchId, id);
      model.broadcast(`exit/${matchId}`, opponent);
    }
    res.clearCookie("match");
    res.status(200).end();
  } else {
    res.status(403).end();
  }
});

router.get("/getmatchid", (req, res) => {
  const matchId = req.cookies.match;
  if (matchId) {
    res.status(200).json({ matchId });
  } else {
    res.status(403).end();
  }
});

router.get("/deletematch", async (req, res) => {
  const matchId = req.cookies.match;
  const id = req.cookies.sessionCookie;
  if (matchId && id) {
    await model.deleteMatchById(matchId, id);
    model.broadcast("cancelmatch", matchId);
    res.clearCookie("match");
    res.status(200).end();
  } else {
    res.status(403).end();
  }
});

export default { router };
