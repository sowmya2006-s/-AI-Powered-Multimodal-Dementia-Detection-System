import Link from "next/link";
import { Button, Container, Typography, Box, Stack } from "@mui/material";

export default function LandingPage() {
    return (
        <Container maxWidth="md">
            <Box sx={{ mt: 8, textAlign: "center" }}>
                <Typography variant="h2" component="h1" gutterBottom fontWeight="bold">
                    Dementia Detection System
                </Typography>
                <Typography variant="h5" color="text.secondary" paragraph>
                    AI-Powered Multimodal Screening for Early Detection
                </Typography>
                <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 4 }}>
                    <Link href="/login" passHref>
                        <Button variant="contained" size="large">
                            Login
                        </Button>
                    </Link>
                    <Link href="/signup" passHref>
                        <Button variant="outlined" size="large">
                            Sign Up
                        </Button>
                    </Link>
                </Stack>
            </Box>
        </Container>
    );
}
