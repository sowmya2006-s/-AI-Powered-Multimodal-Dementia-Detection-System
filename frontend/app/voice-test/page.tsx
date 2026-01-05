import { Container, Typography, Box } from "@mui/material";
import VoiceRecorder from "@/components/VoiceRecorder";

export default function VoiceTestPage() {
    return (
        <Container maxWidth="sm">
            <Box sx={{ py: 6 }}>
                <Typography variant="h4" component="h1" gutterBottom textAlign="center" fontWeight="bold">
                    Phase 1: Voice Dementia Test
                </Typography>
                <Typography variant="body1" textAlign="center" color="text.secondary" sx={{ mb: 4 }}>
                    Please record yourself speaking clearly for about 10-20 seconds.
                    Our AI model will analyze your voice patterns to assess dementia risk.
                </Typography>
                <VoiceRecorder />
            </Box>
        </Container>
    );
}
