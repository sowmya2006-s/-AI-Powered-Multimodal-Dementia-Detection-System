"use client";

import { useState } from "react";
import { Container, Typography, Box, Tabs, Tab } from "@mui/material";
import MemoryVisual from "@/components/MemoryVisual";
import MemoryAudio from "@/components/MemoryAudio";

export default function CognitiveTestPage() {
    const [tab, setTab] = useState(0);

    return (
        <Container maxWidth="md">
            <Box sx={{ py: 6 }}>
                <Typography variant="h4" component="h1" gutterBottom textAlign="center" fontWeight="bold">
                    Phase 2: Cognitive Memory Assessment
                </Typography>
                <Typography variant="body1" textAlign="center" color="text.secondary" sx={{ mb: 4 }}>
                    These tests evaluate your short-term visual and auditory recall abilities.
                </Typography>

                <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
                    <Tabs value={tab} onChange={(_, v) => setTab(v)} centered>
                        <Tab label="Visual Memory" />
                        <Tab label="Auditory Memory" />
                    </Tabs>
                </Box>

                {tab === 0 && <MemoryVisual />}
                {tab === 1 && <MemoryAudio />}
            </Box>
        </Container>
    );
}
