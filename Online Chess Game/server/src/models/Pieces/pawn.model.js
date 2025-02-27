class Pawn {
  static move(x1, y1, x2, y2, turn, attack) {
    let incr = 1;
    if (!turn) {
      incr = -1;
    }

    if (attack) {
      if ((y2 === y1 + 1 || y2 === y1 - 1) && x2 === x1 + incr) {
        return true;
      }
    } else if (
      y2 === y1 &&
      (x2 === x1 + incr ||
        (((x1 === 1 && turn) || (x1 === 6 && !turn)) && x2 === x1 + 2 * incr))
    ) {
      return true;
    }
    return false;
  }
}
export default Pawn;
