
// Récupération des identifiants de l'utilisateur de migration
// Ces valeurs viennent du fichier .env via docker-compose.yml
const migrationUser = process.env.MONGO_MIGRATION_USER;
const migrationPassword = process.env.MONGO_MIGRATION_PASSWORD;

// Récupération des identifiants de l'utilisateur en lecture seule
// Ces valeurs viennent aussi du fichier .env via docker-compose.yml
const readerUser = process.env.MONGO_READER_USER;
const readerPassword = process.env.MONGO_READER_PASSWORD;

db = db.getSiblingDB("healthcare_db");

// Création utilisateur de migration avec les droits de lecture/écriture dans la base healthcare_db

db.createUser({
  user: migrationUser,
  pwd: migrationPassword,
  roles: [
    {
      role: "readWrite",
      db: "healthcare_db"
    }
  ]
});

// Création utilisateur de consultation avec uniquement les droits de lecture
db.createUser({
  user: readerUser,
  pwd: readerPassword,
  roles: [
    {
      role: "read",
      db: "healthcare_db"
    }
  ]
});