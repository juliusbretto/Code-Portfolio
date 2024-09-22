class King {
  static move(x1, y1, x2, y2) {
    if (
      (x2 === x1 + 1 || x2 === x1 - 1 || x2 === x1) &&
      (y2 === y1 + 1 || y2 === y1 - 1 || y2 === y1) &&
      !(x2 === x1 && y2 === y1)
    ) {
      return true;
    }
    return false;
  }
}
export default King;
