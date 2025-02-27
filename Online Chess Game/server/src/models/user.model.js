class User {
  constructor(name, id) {
    this.id = id;
    this.name = name;
  }

  /**
   * Get the id of the user.
   * @returns {String}
   */
  getId() {
    return this.id;
  }

  /**
   * Get the name of the user.
   * @returns {String}
   */
  getName() {
    return this.name;
  }
}
export default User;
