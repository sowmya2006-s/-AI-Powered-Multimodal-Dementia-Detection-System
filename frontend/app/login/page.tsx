"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { TextField, Button, Typography, Container, Box, Paper, Stack } from "@mui/material";
import { z } from "zod";
import axios from "axios";
import Link from "next/link";
import { useRouter } from "next/navigation";

const schema = z.object({
    email: z.string().email("Invalid email address"),
    password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginFormValues = z.infer<typeof schema>;

export default function LoginPage() {
    const router = useRouter();
    const {
        register,
        handleSubmit,
        formState: { errors },
    } = useForm<LoginFormValues>({
        resolver: zodResolver(schema),
    });

    const onSubmit = async (data: LoginFormValues) => {
        try {
            await axios.post("http://localhost:8000/api/accounts/login/", data);
            alert("Login success");
            router.push("/dashboard");
        } catch (error) {
            console.error(error);
            alert("Login failed. Check console for details.");
        }
    };

    return (
        <Container maxWidth="xs">
            <Box sx={{ mt: 8, display: "flex", flexDirection: "column", alignItems: "center" }}>
                <Paper elevation={3} sx={{ p: 4, width: "100%" }}>
                    <Typography component="h1" variant="h5" textAlign="center" gutterBottom>
                        Sign In
                    </Typography>
                    <Box component="form" onSubmit={handleSubmit(onSubmit)} noValidate sx={{ mt: 1 }}>
                        <Stack spacing={2}>
                            <TextField
                                fullWidth
                                label="Email Address"
                                autoComplete="email"
                                autoFocus
                                {...register("email")}
                                error={!!errors.email}
                                helperText={errors.email?.message}
                            />
                            <TextField
                                fullWidth
                                label="Password"
                                type="password"
                                autoComplete="current-password"
                                {...register("password")}
                                error={!!errors.password}
                                helperText={errors.password?.message}
                            />
                            <Button type="submit" fullWidth variant="contained" size="large" sx={{ mt: 2 }}>
                                Login
                            </Button>
                            <Typography variant="body2" textAlign="center">
                                Don&apos;t have an account?{" "}
                                <Link href="/signup" style={{ color: "#1976d2", textDecoration: "none" }}>
                                    Sign Up
                                </Link>
                            </Typography>
                        </Stack>
                    </Box>
                </Paper>
            </Box>
        </Container>
    );
}
