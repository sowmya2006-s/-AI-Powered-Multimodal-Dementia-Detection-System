"use client";

import { Container, Typography, Box, Grid, Card, CardContent, CardActionArea, Stack, Button } from "@mui/material";
import MicIcon from "@mui/icons-material/Mic";
import PsychologyIcon from "@mui/icons-material/Psychology";
import AssessmentIcon from "@mui/icons-material/Assessment";
import Link from "next/link";

export default function DashboardPage() {
    const tests = [
        {
            title: "Voice Test",
            description: "Analyze speech patterns and vocal biomarkers.",
            icon: <MicIcon sx={{ fontSize: 40, color: "#1976d2" }} />,
            link: "/voice-test",
            phase: "Phase 1"
        },
        {
            title: "Medical Report",
            description: "View your latest assessment results and risk scores.",
            icon: <AssessmentIcon sx={{ fontSize: 40, color: "#2e7d32" }} />,
            link: "/report",
            phase: "Summary"
        }
    ];

    return (
        <Container maxWidth="lg">
            <Box sx={{ py: 8 }}>
                <Typography variant="h3" component="h1" gutterBottom fontWeight="bold">
                    Patient Dashboard
                </Typography>
                <Typography variant="h6" color="text.secondary" sx={{ mb: 6 }}>
                    Select an assessment phase to begin or view your previous results.
                </Typography>

                <Grid container spacing={4}>
                    {tests.map((test, index) => (
                        <Grid item xs={12} md={4} key={index}>
                            <Card sx={{ height: "100%", borderRadius: 4, transition: "0.3s", "&:hover": { transform: "translateY(-5px)", boxShadow: 6 } }}>
                                <Link href={test.link} style={{ textDecoration: "none", color: "inherit" }}>
                                    <CardActionArea sx={{ height: "100%", p: 2 }}>
                                        <CardContent>
                                            <Box sx={{ mb: 2 }}>{test.icon}</Box>
                                            <Typography variant="overline" color="text.secondary" fontWeight="bold">
                                                {test.phase}
                                            </Typography>
                                            <Typography variant="h5" component="div" fontWeight="bold" gutterBottom>
                                                {test.title}
                                            </Typography>
                                            <Typography variant="body2" color="text.secondary">
                                                {test.description}
                                            </Typography>
                                        </CardContent>
                                    </CardActionArea>
                                </Link>
                            </Card>
                        </Grid>
                    ))}
                </Grid>
            </Box>
        </Container>
    );
}
