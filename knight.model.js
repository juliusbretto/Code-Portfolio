class Knight {
  static move(x1, y1, x2, y2) {
    if (
      (Math.abs(y2 - y1) === 2 && Math.abs(x2 - x1) === 1) ||
      (Math.abs(y2 - y1) === 1 && Math.abs(x2 - x1) === 2)
    ) {
      return true;
    }
    return false;
  }
}
export default Knight;
