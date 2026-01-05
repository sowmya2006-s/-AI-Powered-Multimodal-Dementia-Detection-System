"use client";

import { useState } from "react";
import { Box, Button, Typography, Paper, Grid, CircularProgress } from "@mui/material";
import { motion } from "framer-motion";
import api from "@/lib/api";

export default function MemoryVisual() {
    const [round, setRound] = useState(0);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(false);
    const [started, setStarted] = useState(false);
    const [finished, setFinished] = useState(false);
    const [result, setResult] = useState<any>(null);
    const [showTarget, setShowTarget] = useState(false);

    const startTest = async () => {
        setLoading(true);
        setRound(0);
        try {
            const patientId = 1;
            await api.post("/cognitive/start/", {
                patient_id: patientId,
                test_mode: "visual"
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
        setShowTarget(false);
        try {
            const res = await api.get("/cognitive/generate-round/");
            const json = res.data;

            if (json.completed) {
                finishTest();
            } else {
                setData(json);
                setRound(json.round);
                setShowTarget(true);
                setTimeout(() => setShowTarget(false), 3000);
            }
        } catch (err) {
            console.error("Fetch round error", err);
            finishTest();
        } finally {
            setLoading(false);
        }
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
                <Typography variant="h5" gutterBottom fontWeight="bold">Visual Test Results</Typography>
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
                <Typography variant="body1" sx={{ mb: 2 }}>You will see 4 rounds. Memorize the image shown, then pick it from the options.</Typography>
                <Button variant="contained" size="large" onClick={startTest} disabled={loading}>
                    {loading ? "Starting..." : "Start Visual Memory Test"}
                </Button>
            </Box>
        );
    }

    if (loading && !data) return <Box sx={{ textAlign: "center", mt: 4 }}><CircularProgress /></Box>;
    if (!data) return <Typography>Error loading game.</Typography>;

    return (
        <Box sx={{ maxWidth: 600, mx: "auto", mt: 2 }}>
            <Paper sx={{ p: 4, textAlign: "center", borderRadius: 4 }}>
                <Typography variant="h6" gutterBottom color="primary">
                    Round {round} / 4
                </Typography>

                {showTarget ? (
                    <Box sx={{ mb: 4, textAlign: "center" }}>
                        <Typography variant="body1" sx={{ mb: 2 }}>MEMORIZE THIS IMAGE</Typography>
                        <motion.img
                            key={data.target}
                            initial={{ opacity: 0, scale: 0.8 }}
                            animate={{ opacity: 1, scale: 1 }}
                            src={`http://localhost:8000${data.target}`}
                            style={{ width: 250, height: 250, borderRadius: 8, objectFit: "cover", border: "4px solid #1976d2" }}
                        />
                    </Box>
                ) : (
                    <>
                        <Typography variant="body1" sx={{ mb: 3 }}>
                            Pick the image you just saw:
                        </Typography>

                        <Grid container spacing={2}>
                            {data.options.map((opt: string, index: number) => (
                                <Grid item xs={6} key={index}>
                                    <Button
                                        fullWidth
                                        onClick={() => submit(opt)}
                                        disabled={loading}
                                        sx={{ p: 1, border: "2px solid #e0e0e0", "&:hover": { border: "2px solid #1976d2" } }}
                                    >
                                        <img
                                            src={`http://localhost:8000${opt}`}
                                            style={{ width: "100%", height: 120, objectFit: "cover", borderRadius: 4 }}
                                            onError={(e) => { (e.target as HTMLImageElement).src = 'https://via.placeholder.com/120?text=Option'; }}
                                        />
                                    </Button>
                                </Grid>
                            ))}
                        </Grid>
                    </>
                )}
            </Paper>
        </Box>
    );
}
