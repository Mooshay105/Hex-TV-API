import { ResultSet } from "@libsql/client";
import { getDbConnection } from "./databaseConnection";

async function getVideos(category: string) {
	const dbResults: ResultSet = await getDbConnection(true).execute({
		sql: "SELECT * FROM videos WHERE category = ?",
		args: [category],
	});

	const rows = dbResults.rows || [];

	const results = rows.map((row) => ({
		id: row[0],
		name: row[1],
		description: row[2],
		thumbnailURL: row[3],
		videoURL: row[4],
		date: row[5],
		urlName: row[6],
		rating: row[7],
		category: row[8],
	}));

	return results;
}

async function getVideosForSearch(query: string) {
	const dbResults: ResultSet = await getDbConnection(true).execute({
		sql: "SELECT * FROM videos WHERE name LIKE ?",
		args: [`%${query}%`],
	});

	const rows = dbResults.rows || [];

	const results = rows.map((row) => ({
		id: row[0],
		name: row[1],
		description: row[2],
		thumbnailURL: row[3],
		videoURL: row[4],
		date: row[5],
		urlName: row[6],
		rating: row[7],
		category: row[8],
	}));

	return results;
}

async function addVideo(data: any) {
	const date = Date().toString().split("T")[0];
	const dbResults: ResultSet = await getDbConnection(false).execute({
		sql: "INSERT INTO videos (name, description, thumbnailURL, videoURL, date, urlName, rating, category) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
		args: [
			data.name,
			data.description,
			data.thumbnailURL,
			data.videoURL,
			date,
			data.urlName,
			data.ageRating,
			data.category,
		],
	});

	return dbResults.rowsAffected > 0;
}

async function deleteVideo(data: any) {
	const urlName = data.urlName;
	const dbResults: ResultSet = await getDbConnection(false).execute({
		sql: "DELETE FROM videos WHERE urlName = ?",
		args: [urlName],
	});

	return dbResults.rowsAffected > 0;
}

export { getVideos, getVideosForSearch, addVideo, deleteVideo };
