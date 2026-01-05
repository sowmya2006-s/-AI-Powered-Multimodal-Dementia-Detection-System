"use client";

import { useState } from "react";
import { Box, Button, Typography, Paper, Stack, CircularProgress } from "@mui/material";
import PlayArrowIcon from "@mui/icons-material/PlayArrow";
import { Howl } from "howler";
import api from "@/lib/api";

export default function MemoryAudio() {
    const [round, setRound] = useState(0);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [started, setStarted] = useState(false);
    const [finished, setFinished] = useState(false);
    const [result, setResult] = useState<any>(null);

    const startTest = async () => {
        setLoading(true);
        setRound(0);
        try {
            const patientId = 1;
            await api.post("/cognitive/start/", {
                patient_id: patientId,
                test_mode: "audio"
            });
            setStarted(true);
            fetchRound();
        } catch (err) {
            console.error("Start test error", err);
            alert("Failed to start test. Check console.");
        } finally {
            setLoading(false);
        }
    };

    const fetchRound = async () => {
        setLoading(true);
        try {
            const res = await api.get("/cognitive/generate-round/");
            const json = res.data;
            if (json.completed) {
                finishTest();
            } else {
                setData(json);
                setRound(json.round);
            }
        } catch (err) {
            console.error("Fetch round error", err);
            finishTest();
        } finally {
            setLoading(false);
        }
    };

    const play = (src: string) => {
        const sound = new Howl({ src: [`http://localhost:8000${src}`] });
        sound.play();
    };

    const submit = async (choice: string) => {
        setLoading(true);
        try {
            const res = await api.post("/cognitive/submit-answer/", { answer: choice });
            const json = res.data;
            if (json.next_round) {
                fetchRound();
            } else {
                finishTest();
            }
        } catch (err) {
            console.error("Submit answer error", err);
        } finally {
            setLoading(false);
        }
    };

    const finishTest = async () => {
        setLoading(true);
        try {
            const res = await api.post("/cognitive/finish/");
            setResult(res.data);
            setFinished(true);
        } catch (err) {
            console.error("Finish test error", err);
            setResult({ accuracy: 0, risk_level: "ERROR" });
            setFinished(true);
        } finally {
            setLoading(false);
        }
    };

    if (finished) {
        return (
            <Paper sx={{ p: 4, textAlign: "center", borderRadius: 4 }}>
                <Typography variant="h5" gutterBottom fontWeight="bold">Auditory Test Results</Typography>
                <Typography variant="h6">Accuracy: {result?.accuracy !== undefined ? (result.accuracy * 100).toFixed(0) : 0}%</Typography>
                <Typography variant="h6" color={result?.risk_level === 'LOW' ? 'success.main' : 'error.main'}>
                    Risk Level: {result?.risk_level || "UNKNOWN"}
                </Typography>
                <Button variant="contained" sx={{ mt: 3 }} onClick={() => window.location.href = '/dashboard'}>
                    Back to Dashboard
                </Button>
            </Paper>
        );
    }

    if (!started) {
        return (
            <Box sx={{ textAlign: "center", mt: 4 }}>
                <Typography variant="body1" sx={{ mb: 2 }}>You will hear various sounds. Listen carefully and pick the correct one from the options.</Typography>
                <Button variant="contained" size="large" color="secondary" onClick={startTest} disabled={loading}>
                    {loading ? "Starting..." : "Start Auditory Memory Test"}
                </Button>
            </Box>
        );
    }

    if (loading && !data) return <Box sx={{ textAlign: "center", mt: 4 }}><CircularProgress /></Box>;
    if (!data) return <Typography>Error loading game.</Typography>;

    return (
        <Box sx={{ maxWidth: 600, mx: "auto", mt: 2 }}>
            <Paper sx={{ p: 4, textAlign: "center", borderRadius: 4 }}>
                <Typography variant="h6" gutterBottom color="secondary">
                    Auditory Round {round} / 4
                </Typography>
                <Typography variant="body1" sx={{ mb: 3 }}>
                    Listen to the options and pick the sound you heard.
                </Typography>

                <Stack spacing={2}>
                    {data.options.map((audio: string, index: number) => (
                        <Box key={index} sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                            <Button
                                variant="outlined"
                                startIcon={<PlayArrowIcon />}
                                onClick={() => play(audio)}
                            >
                                Play Sound {index + 1}
                            </Button>
                            <Button
                                variant="contained"
                                onClick={() => submit(audio)}
                                disabled={loading}
                                sx={{ flexGrow: 1 }}
                            >
                                Select This Sound
                            </Button>
                        </Box>
                    ))}
                </Stack>
            </Paper>
        </Box>
    );
}
