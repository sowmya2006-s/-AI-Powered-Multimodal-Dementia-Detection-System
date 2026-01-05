"use client";

import { useState, useRef } from "react";
import { Button, Box, Typography, Paper, CircularProgress, IconButton, Stack } from "@mui/material";
import MicIcon from "@mui/icons-material/Mic";
import StopIcon from "@mui/icons-material/Stop";
import CloudUploadIcon from "@mui/icons-material/CloudUpload";
import api from "@/lib/api";

export default function VoiceRecorder() {
    const [recording, setRecording] = useState(false);
    const [audioUrl, setAudioUrl] = useState<string | null>(null);
    const [audioBlob, setAudioBlob] = useState<Blob | null>(null);
    const [uploading, setUploading] = useState(false);
    const mediaRecorderRef = useRef<MediaRecorder | null>(null);

    const startRecording = async () => {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            const mediaRecorder = new MediaRecorder(stream);
            mediaRecorderRef.current = mediaRecorder;

            const chunks: BlobPart[] = [];
            mediaRecorder.ondataavailable = (e) => {
                if (e.data.size > 0) {
                    chunks.push(e.data);
                }
            };

            mediaRecorder.onstop = () => {
                const blob = new Blob(chunks, { type: "audio/wav" });
                setAudioBlob(blob);
                setAudioUrl(URL.createObjectURL(blob));
            };

            mediaRecorder.start();
            setRecording(true);
            setAudioUrl(null);
            setAudioBlob(null);
        } catch (err) {
            console.error("Error accessing microphone", err);
            alert("Error accessing microphone. Please ensure permissions are granted.");
        }
    };

    const stopRecording = () => {
        if (mediaRecorderRef.current && recording) {
            mediaRecorderRef.current.stop();
            setRecording(false);
            mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
        }
    };

    const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            setAudioBlob(file);
            setAudioUrl(URL.createObjectURL(file));
            setResult(null);
        }
    };

    const fileInputRef = useRef<HTMLInputElement>(null);

    const [result, setResult] = useState<any>(null);

    const upload = async () => {
        if (!audioBlob) return;
        setUploading(true);
        const formData = new FormData();
        formData.append("audio_file", audioBlob, "voice_test.wav");
        formData.append("patient", "1"); // Demo patient ID

        try {
            const response = await api.post("/voice/upload/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            if (response.status === 201 || response.status === 200) {
                setResult(response.data);
                alert("Voice analyzed successfully!");
            } else {
                alert("Upload failed.");
            }
        } catch (error) {
            console.error("Upload error", error);
            alert("Error uploading voice. Check console.");
        } finally {
            setUploading(false);
        }
    };

    return (
        <Paper elevation={2} sx={{ p: 4, borderRadius: 2, textAlign: "center" }}>
            <Typography variant="h6" gutterBottom>
                Voice Assessment
            </Typography>

            {result ? (
                <Box sx={{ p: 3, bgcolor: "#f5f5f5", borderRadius: 2, mb: 3 }}>
                    <Typography variant="h5" fontWeight="bold" color="primary">Results</Typography>
                    <Typography variant="h6" sx={{ mt: 1 }}>Risk Level: <strong>{result.risk_level}</strong></Typography>
                    <Typography variant="body1">Dementia Probability: <strong>{result.probability}</strong></Typography>
                    <Button variant="outlined" sx={{ mt: 2 }} onClick={() => setResult(null)}>New Test</Button>
                </Box>
            ) : (
                <>
                    <Box sx={{ my: 3 }}>
                        <Stack direction="row" spacing={3} justifyContent="center" alignItems="center">
                            {!recording ? (
                                <IconButton
                                    color="primary"
                                    onClick={startRecording}
                                    sx={{ width: 80, height: 80, backgroundColor: "#e3f2fd" }}
                                >
                                    <MicIcon sx={{ fontSize: 40 }} />
                                </IconButton>
                            ) : (
                                <IconButton
                                    color="error"
                                    onClick={stopRecording}
                                    sx={{ width: 80, height: 80, backgroundColor: "#ffebee" }}
                                >
                                    <StopIcon sx={{ fontSize: 40 }} />
                                </IconButton>
                            )}

                            {!recording && (
                                <>
                                    <input
                                        type="file"
                                        accept="audio/*"
                                        hidden
                                        ref={fileInputRef}
                                        onChange={handleFileChange}
                                    />
                                    <IconButton
                                        color="secondary"
                                        onClick={() => fileInputRef.current?.click()}
                                        sx={{ width: 80, height: 80, backgroundColor: "#f3e5f5" }}
                                    >
                                        <CloudUploadIcon sx={{ fontSize: 40 }} />
                                    </IconButton>
                                </>
                            )}
                        </Stack>
                    </Box>
                    <Typography variant="body2" color="text.secondary">
                        {recording ? "Recording... Click stop when finished." : "Click microphone to record or cloud to upload audio."}
                    </Typography>

                    {audioUrl && !recording && (
                        <Box sx={{ mt: 3 }}>
                            <audio src={audioUrl} controls style={{ width: "100%" }} />
                            <Button
                                variant="contained"
                                color="success"
                                startIcon={uploading ? <CircularProgress size={20} color="inherit" /> : <CloudUploadIcon />}
                                onClick={upload}
                                disabled={uploading}
                                sx={{ mt: 2 }}
                                fullWidth
                            >
                                {uploading ? "Analyzing..." : "Analyze Dementia Risk"}
                            </Button>
                        </Box>
                    )}
                </>
            )}
        </Paper>
    );
}
