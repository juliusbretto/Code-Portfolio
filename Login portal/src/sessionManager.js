import { v4 as uuidv4 } from "uuid";

class SessionManager {
  constructor() {
    this.sessions = new Map();
    this.usernames = new Map();
  }

  sessionExists(id) {
    return this.sessions.has(id);
  }

  findSessionById(id) {
    return this.sessions.get(id);
  }

  createNewSession(username) {
    const id = uuidv4();
    this.sessions.set(id, { id });
    this.usernames.set(id, username);
    return this.findSessionById(id);
  }
  
  deleteSession(id) {
	  this.sessions.delete(id);
	  this.usernames.delete(id);
  }
  
  findUsername(id) {
	  return this.usernames.get(id);
  }
  
  
  getNbrOfSessions(username) {
//skapar en array med session-ids för alla usernames, och filtrerar så att endast de ids som är förknippade med username är kvar
	  return Array.from(this.usernames.values()).filter((value) => value === username).length;
}
  
  deleteOtherSessions(id) {
	  const username = this.usernames.get(id);
	  const sessionIds = Array.from(this.sessions.keys()); //får alla session-ids

	  sessionIds.forEach((session) => { //för varje session i sessionIds
		//om användarnamnen stämmer överens, samt att vår nuvarande session inte är lika med id (den ska behållas)
	    if (this.usernames.get(session) === username && id !== session) {
	      this.deleteSession(session); //raderas sessionen
	    }
	  });
}
  
}

export default new SessionManager();
