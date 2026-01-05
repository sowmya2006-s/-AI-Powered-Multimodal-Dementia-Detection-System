"use client";

import { useEffect, useState } from "react";
import { Container, Typography, Box, Paper, Divider, Grid, CircularProgress, Button } from "@mui/material";
import RiskBadge from "@/components/RiskBadge";

export default function ReportPage() {
    const [report, setReport] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchReport = async () => {
            try {
                const patientId = 1; // Demo patient_id
                const res = await fetch("http://localhost:8000/api/reports/generate-fusion/", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ patient_id: patientId }),
                });
                const json = await res.json();
                setReport(json);
            } catch (err) {
                console.error("Error fetching report", err);
            } finally {
                setLoading(false);
            }
        };

        fetchReport();
    }, []);

    if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 10 }}><CircularProgress /></Box>;

    if (!report || report.error) {
        return (
            <Container maxWidth="md">
                <Box sx={{ py: 8, textAlign: 'center' }}>
                    <Typography variant="h5" color="error">
                        {report?.error || "Error generating report. Ensure all tests are completed."}
                    </Typography>
                    <Button variant="contained" sx={{ mt: 3 }} onClick={() => window.location.href = '/dashboard'}>
                        Back to Dashboard
                    </Button>
                </Box>
            </Container>
        );
    }

    return (
        <Container maxWidth="md">
            <Box sx={{ py: 8 }}>
                <Paper elevation={3} sx={{ p: 6, borderRadius: 4 }}>
                    <Typography variant="h4" gutterBottom fontWeight="bold">
                        Multimodal Assessment Report
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                        Assessment Date: {new Date().toLocaleDateString()}
                    </Typography>

                    <Divider sx={{ my: 4 }} />

                    <Grid container spacing={4}>
                        <Grid item xs={12} md={6}>
                            <Typography variant="h6" fontWeight="bold">
                                Phase 1: Voice Analysis
                            </Typography>
                            <Typography variant="body1">
                                Dementia Score: <strong>{report.voice_score != null ? report.voice_score.toFixed(2) : "N/A"}</strong>
                            </Typography>
                        </Grid>

                        <Grid item xs={12} md={6}>
                            <Typography variant="h6" fontWeight="bold">
                                Phase 2: Cognitive Test (Archived)
                            </Typography>
                            <Typography variant="body1">
                                Memory Accuracy: <strong>{report.cognitive_score != null ? (report.cognitive_score * 100).toFixed(0) + "%" : "N/A"}</strong>
                            </Typography>
                        </Grid>
                    </Grid>

                    <Divider sx={{ my: 4 }} />

                    <Box sx={{ textAlign: "center", p: 4, bgcolor: report.mri_triggered ? "#fff5f5" : "#f5fff5", borderRadius: 4, border: report.mri_triggered ? "2px solid #ffcdd2" : "2px solid #c8e6c9" }}>
                        <Typography variant="h5" gutterBottom fontWeight="bold">
                            Integrated Risk Level
                        </Typography>
                        <RiskBadge level={report.overall_risk} />

                        <Typography variant="body1" sx={{ mt: 3, fontWeight: "medium" }}>
                            Recommendation:
                        </Typography>
                        <Typography variant="body1" color={report.mri_triggered ? "error.main" : "text.primary"} sx={{ mt: 1 }}>
                            {report.recommendation}
                        </Typography>

                        {report.mri_triggered && (
                            <Box sx={{ mt: 3, p: 2, bgcolor: "#d32f2f", color: "white", borderRadius: 2 }}>
                                <Typography variant="h6">⚠️ Phase 3 MRI Check Recommended</Typography>
                            </Box>
                        )}
                    </Box>

                    <Box sx={{ mt: 4, textAlign: "center" }}>
                        <Button variant="outlined" onClick={() => window.location.href = '/dashboard'}>
                            Return to Dashboard
                        </Button>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}
