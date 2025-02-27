class Bishop {
  static move(x1, y1, x2, y2) {
    if (Math.abs(x2 - x1) === Math.abs(y2 - y1) && !(x2 === x1 && y2 === y1)) {
      return true;
    }
    return false;
  }
}
export default Bishop;
